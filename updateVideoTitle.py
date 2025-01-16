import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

def changeVideoTitle(viewCount, id, c):
    title = "Este vídeo tiene " + str(viewCount) + " Visitas"
    desc = "¿Estás impresionado?"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Sólo para pruebas locales

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Obtener credenciales y crear un cliente de la API
    flow = c.flow if c.flow else google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    c.flow = flow

    auth_url, _ = flow.authorization_url(prompt='consent', redirect_uri="http://localhost:8080/")
    print("Go to this URL and authorize the application:", auth_url)

    code = input("Enter the authorization code: ")
    credentials = flow.fetch_token(authorization_response=code)
    c.credentials = credentials

    youtube = c.youtube if c.youtube else googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    c.youtube = youtube

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
    print(response)
