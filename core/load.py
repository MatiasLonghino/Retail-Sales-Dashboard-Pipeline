import pandas as pd
import io
import os

from connectors.drive.operations import upload_csv_to_drive
#LOAD
def save_csv_local(df, path):
    df.to_csv(path, index=False, sep=';', encoding='utf-8-sig')
    
def load(datasets: dict):
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    folder_id = os.getenv("LOAD_FOLDER_ID")
    
    #print(f"DEBUG: Subiendo a la carpeta ID: {folder_id}")

    uploaded_files = {}

    for name, df in datasets.items():
        byte_buffer = io.BytesIO()        
        df.to_csv(byte_buffer, index=False, encoding='utf-8')

        byte_buffer.seek(0)

        # Subida
        file_id = upload_csv_to_drive(
            buffer=byte_buffer,
            filename=name,
            credentials_path=credentials_path,
            folder_id=folder_id
        )

        uploaded_files[name] = file_id

    return uploaded_files #Devuelve la direccion de cada archivo en el drive