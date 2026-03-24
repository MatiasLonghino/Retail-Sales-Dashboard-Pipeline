import io
import os

from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

from connectors.drive.client import GoogleDriveClient
from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ["https://www.googleapis.com/auth/drive"]


# Factory interna
def _get_service(credentials_path: str):
    client = GoogleDriveClient(credentials_path, SCOPES)
    return client.get_service()


# Buscar archivo
def _get_file_id(service, filename: str, folder_id: str):
    # Añadimos 'parents' a la query para limitar la búsqueda a esa carpeta
    query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
    
    results = service.files().list(
        q=query,
        fields="files(id, name)",
        # Opcional: spaces='drive' asegura que busque en el drive estándar
        spaces='drive' 
    ).execute()

    files = results.get("files", [])
    
    if files:
        # Log opcional para confirmar dónde se encontró
        #print(f"Archivo encontrado: {files[0]['name']} con ID: {files[0]['id']}")
        return files[0]["id"]
    
    print(f"No se encontró el archivo '{filename}' en la carpeta especificada.")
    return None # Si hay algo en files devuelve el file_id primero, caso contrario devuelve un None
# En el metodo get file id, hay un detalle. En google drive, si se puede tener archivos con el mismo nombre por lo que se podria requerir mas filtros como podria ser uno por fecha de creacion

# Descargar archivo como buffer
def _download_file(service, file_id: str) -> io.BytesIO: #Promete en devolver un objeto io.BytesIO(archivo que vive en ram)
    request = service.files().get_media(fileId=file_id)#Se le indica a la api que solo se quiere el contenido binario y no los metadatos

    buffer = io.BytesIO()#contenedor vacio
    downloader = MediaIoBaseDownload(buffer, request)

    done = False
    while not done:#Google hace el envio por partes, chunks, del file para evitar un colapso
        _, done = downloader.next_chunk()

    buffer.seek(0) #Mueve el curso de lectura al inicio
    return buffer


# Subir archivo desde buffer
import time
import random

def _upload_file(service, buffer: io.BytesIO, filename: str, mime_type: str, folder_id: str = None):
    # El mimeType dentro de 'metadata' le dice a Drive cómo guardarlo
    metadata = {
        "name": filename,
        "mimeType": mime_type  # Ahora dinámico (será "text/csv")
    }
    
    if folder_id:
        metadata["parents"] = [folder_id]

    buffer.seek(0)
    # MediaIoBaseUpload también debe llevar el tipo de contenido correcto
    media = MediaIoBaseUpload(buffer, mimetype=mime_type, resumable=True)

    for n in range(3): 
        try:
            # Si quieres evitar que Google lo convierta, asegúrate de NO usar
            # el parámetro opcional 'convert=True' (por defecto es False)
            file = service.files().create(
                body=metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True 
            ).execute()

            time.sleep(2) 
            return file.get("id")

        except Exception as e:
            if "storageQuotaExceeded" in str(e) and n < 2:
                wait_time = (2 ** n) + random.random()
                print(f"DEBUG: Error de cuota detectado. Reintentando en {wait_time:.2f}s...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Error crítico en la subida de {filename}: {e}")
                raise

#Manejo de buffer
def get_drive_buffer(filename, credentials_path, folder_id=None):
    service = _get_service(credentials_path)
    file_id = _get_file_id(service, filename, folder_id)

    if not file_id:
        raise FileNotFoundError(...)

    return _download_file(service, file_id)

def upload_csv_to_drive(buffer, filename, credentials_path, folder_id=None):
    service = _get_service(credentials_path)

    # Cambiamos el mime_type a text/csv para que Drive lo trate como un archivo plano
    return _upload_file(
        service=service,
        buffer=buffer,
        filename=filename,
        mime_type="text/csv", 
        folder_id=folder_id
    )
    
    
    

        
        
##### auxiliares ######
def get_badId():
    service = _get_service(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    results = service.files().list(pageSize=10, fields="files(id, name, quotaBytesUsed)").execute()
    for f in results.get('files', []):
        print(f"ID: {f['id']} | Nombre: {f['name']} | Tamaño: {f.get('quotaBytesUsed')} bytes")
        
def delete_badId():
    # SUSTITUYE EL ID DE ABAJO POR EL QUE TE SALIÓ ARRIBA
    file_id_real = "18GkArPxgXHJlWvJ6HeVm5Fs4mp_ojH96" 
    service = _get_service(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    try:
        service.files().delete(fileId=file_id_real).execute()
        print("¡Libertad! Archivo borrado y cuota recuperada.")
    except Exception as e:
        print(f"Error al borrar: {e}")
        
        
def clean_service_account_storage():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    """
    Busca y elimina todos los archivos donde la Service Account es OWNER.
    Esto libera la cuota de 0 bytes que bloquea el error 403.
    """
    # 1. Autenticación
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    print("--- Iniciando limpieza de Service Account ---")

    try:
        # 2. Buscamos archivos donde la cuenta es DUEÑA ('me' in owners)
        # Esto incluye archivos huérfanos que no ves en tu Drive personal
        query = "'me' in owners"
        results = service.files().list(
            q=query, 
            fields="files(id, name, size, quotaBytesUsed)"
        ).execute()
        
        files = results.get('files', [])

        if not files:
            print("Resultado: La Service Account no tiene archivos propios. Está limpia.")
            return

        print(f"Se encontraron {len(files)} archivos ocupando espacio:")
        
        for f in files:
            f_id = f['id']
            f_name = f['name']
            f_size = f.get('quotaBytesUsed', '0')
            
            print(f"Eliminando: {f_name} ({f_size} bytes)...", end=" ")
            
            # 3. Eliminación permanente (salta la papelera)
            service.files().delete(fileId=f_id).execute()
            print("✅ Borrado.")

        print("\n--- Limpieza completada. La cuota debería ser ahora 0/0 ---")

    except Exception as e:
        print(f"\n❌ Error durante la limpieza: {e}")