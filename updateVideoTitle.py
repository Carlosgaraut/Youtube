import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

def authenticate_with_oauth2(client_secrets_file, scopes):
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Configura el flujo de OAuth 2.0
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    # Solicita el código de autorización
    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"Go to the following URL to authorize the application: {auth_url}")
    
    # Ingresar el código de autorización manualmente
    authorization_response = input("Enter the authorization code: ")
    credentials = flow.fetch_token(
        'https://oauth2.googleapis.com/token', 
        authorization_response=authorization_response)
    
    return credentials

def update_video_title(credentials, video_id, new_title, new_description):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    request = youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": new_title,
                "description": new_description,
                "categoryId": "22"
            }
        }
    )

    response = request.execute()
    return response

def main():
    client_secrets_file = 'client_secret.json'  # Ruta al archivo de credenciales
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Autenticación
    credentials = authenticate_with_oauth2(client_secrets_file, scopes)

    # Cambiar título y descripción del video
    video_id = "7lqYwKU3WM4"  # El ID del video que quieres modificar
    new_title = "Este vídeo tiene nuevas visitas"
    new_description = "¡Mira el vídeo para más detalles!"
    
    response = update_video_title(credentials, video_id, new_title, new_description)
    print(response)

if __name__ == '__main__':
    main()
