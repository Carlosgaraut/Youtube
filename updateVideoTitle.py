import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import time

# Clase para manejar las credenciales y el flujo de autorización
class creds:
    def __init__(self):
        self.credentials = False
        self.flow = False
        self.youtube = False
        self.viewCount = 0
        self.num = 0


def changeVideoTitle(viewCount, id, c):
    # Título y descripción del video
    title = "Este vídeo tiene " + str(viewCount) + " Visitas"
    desc = "¿Estás impresionado?"

    # Alcance necesario para la API de YouTube
    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    # Desactiva la verificación HTTPS (solo para pruebas locales)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"  # Asegúrate de que este archivo esté en tu directorio

    # Crear el flujo de autorización
    flow = c.flow if c.flow else google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    c.flow = flow

    try:
        # Obtener el enlace de autorización
        auth_url, _ = flow.authorization_url(access_type='offline')
        print(f"Por favor visita esta URL para autorizar la aplicación:\n{auth_url}")
        
        # Pide al usuario que pegue el código de autorización aquí
        auth_code = input("Introduce el código de autorización: ")

        # Intercambiar el código por un token de acceso
        credentials = flow.fetch_token(authorization_response=f'http://localhost:8888/?code={auth_code}')
        c.credentials = credentials

    except Exception as e:
        print(f"Error al intentar autorizar desde la consola: {e}")
        return

    # Crear cliente de YouTube
    youtube = c.youtube if c.youtube else googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    c.youtube = youtube

    # Actualizar título del video
    request = youtube.videos().update(
        part="snippet",
        body={
            "id": id,
            "snippet": {
                "categoryId": 22,
                "description": desc,
                "title": title
            },
        }
    )

    response = request.execute()

    print("Video actualizado con éxito:", response)


def main():
    # Ejemplo: id de video y viewCount
    viewCount = 137
    video_id = "7lqYwKU3WM4"
    
    # Objeto 'c' donde almacenamos las credenciales y el cliente
    c = type('', (), {})()  # Crear objeto vacío
    c.credentials = None
    c.flow = None
    c.youtube = None

    changeVideoTitle(viewCount, video_id, c)

if __name__ == "__main__":
    main()
