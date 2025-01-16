import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def changeVideoTitle(viewCount, video_id, c):
    # Formatea el título y la descripción con el número de visitas
    title = f"Este vídeo tiene {viewCount} visitas"
    desc = "¿Estás impresionado?"

    # Alcance de las credenciales de la API de YouTube
    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    # Desactiva la verificación HTTPS de OAuthlib (solo para desarrollo local)
    # *NO* dejes esta opción habilitada en producción
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Obtiene las credenciales y crea un cliente API
    if not c.flow:
        c.flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)

    # Si ya se tienen credenciales, usar eso, sino pedir autorización
    if not c.credentials:
        auth_url, _ = c.flow.authorization_url(prompt='consent')
        print("Go to this URL and authorize the application:", auth_url)
        code = input("Enter the authorization code: ")
        c.credentials = c.flow.fetch_token(authorization_response=code)

    # Si las credenciales no están inicializadas, se hace el proceso de autorización
    youtube = c.youtube if c.youtube else googleapiclient.discovery.build(
        api_service_name, api_version, credentials=c.credentials)
    c.youtube = youtube

    # Crear el request para actualizar el título del video
    request = youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "categoryId": 22,  # Puede cambiar dependiendo de la categoría del video
                "description": desc,
                "title": title
            }
        }
    )

    # Ejecutar el request para actualizar el video
    response = request.execute()
    print(f"Video title updated: {response}")
