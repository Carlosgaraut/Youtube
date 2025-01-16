import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def changeVideoTitle(viewCount, id, c):
    title = "Este vídeo tiene " + str(viewCount) + " Visitas wouuu"
    desc = "¿Estás impresionado?"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = c.flow if c.flow else google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    c.flow = flow

    # Usar el flujo de consola para obtener las credenciales
    try:
        credentials = c.credentials if c.credentials else flow.run_console()  # Usamos run_console() en la consola
        c.credentials = credentials
    except Exception as e:
        print("Error al intentar autorizar desde la consola: ", e)
        return

    # Crear cliente API de YouTube
    youtube = c.youtube if c.youtube else googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    c.youtube = youtube

    # Actualizar el título del vídeo
    request = youtube.videos().update(
        part="snippet",  # ,status
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
    print(response)  # Muestra la respuesta de la API

