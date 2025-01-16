import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def changeVideoTitle(viewCount, id, c):
    title = "Este vídeo tiene " + str(viewCount) + " Visitas"
    desc = "¿Estás impresionado?"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Asegúrate de estar trabajando en local

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"  # El archivo JSON debe estar correctamente configurado

    # Get credentials and create an API client
    flow = c.flow if c.flow else google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    c.flow = flow

    # Solicitar la URL de autorización
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline'  # Asegúrate de agregar esto para obtener el refresh token
    )

    # Mostrar la URL y pedir el código de autorización
    print("Go to this URL and authorize the application:", auth_url)
    code = input("Enter the authorization code: ")

    # Obtener el token
    credentials = flow.fetch_token(authorization_response=code)
    c.credentials = credentials

    youtube = c.youtube if c.youtube else googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    c.youtube = youtube

    # Realizar la actualización del título del video
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
    print(response)
