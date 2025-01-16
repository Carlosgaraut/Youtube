import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def changeVideoTitle(viewCount, id, c):
    title = "Este vídeo tiene " + str(viewCount) + " Visitas"
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

    # Use run_local_server() instead of run_console()
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline',  # Asegúrate de agregar esto para obtener el refresh token
        redirect_uri="http://localhost:8888/"  # Asegúrate de que el puerto coincida aquí
    )
    
    print("Go to this URL and authorize the application:", auth_url)
    code = input("Enter the authorization code: ")
    credentials = flow.fetch_token(authorization_response=code)
    c.credentials = credentials

    youtube = c.youtube if c.youtube else googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    c.youtube = youtube

    request = youtube.videos().update(
        part="snippet",  # ,status
        body={
            "id": id,
            "snippet": {
                "categoryId": 22,
                # "defaultLanguage": "en",
                "description": desc,
                # "tags": [
                #   "tom scott","tomscott","api","coding","application programming interface","data api"
                # ],
                "title": title
            },
        }
    )
    response = request.execute()
    print(response)

