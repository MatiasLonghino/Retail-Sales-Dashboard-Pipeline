from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os


class GoogleDriveClient:
    """
    Cliente encargado de autenticarse contra Google Drive API
    y proveer el objeto service reutilizable.
    """

    def __init__(self, credentials_path: str, scopes: list[str]):# Es un constructor
        #self._service = None----> Esta es la clave del rendimiento. Se inicializa en None para indicar que la conexión aún no ha sido creada.
        #credentials_path----> La ruta al archivo JSON que contiene las llaves secretas de tu "Service Account" de Google Cloud.
        #scopes----> Define qué permisos tendrá tu aplicación (por ejemplo, solo lectura, o control total de archivos)
        self.credentials_path = credentials_path
        self.scopes = scopes
        self._service = None

    def _authenticate(self):
        creds = None
        # El archivo token.pickle guarda tu sesión para no loguearte cada vez
        token_path = 'config/secrets/token.pickle'
    
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
            
        # Si no hay credenciales válidas, pedimos login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                     os.getenv("GOOGLE_APPLICATION_CLIENT_CREDENTIAL"), self.scopes)
                # Esto abrirá una pestaña en tu navegador
                creds = flow.run_local_server(port=0)
            
            # Guardamos el token para la próxima vez
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            
        return creds

    def get_service(self):
        """
        Devuelve una instancia del servicio de Google Drive.
        Se inicializa una sola vez (lazy loading).
        """
        if self._service is None:
            credentials = self._authenticate()
            self._service = build("drive", "v3", credentials=credentials)

        return self._service




