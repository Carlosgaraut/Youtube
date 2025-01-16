from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle

# Ruta del archivo de credenciales (client_secret.json)
CLIENT_SECRET_FILE = 'client_secret.json'

# Alcance de la autorización
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def changeVideoTitle(viewCount, video_id, youtube):
    # Inicia el flujo de autenticación
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    
    # Si no tienes un token guardado, pide la autorización
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            auth_url, _ = flow.authorization_url(prompt='consent')  # Eliminamos el `redirect_uri`
            print('Go to this URL and authorize the application: {}'.format(auth_url))
            authorization_response = input('Enter the authorization code: ')
            credentials = flow.fetch_token(
                'https://oauth2.googleapis.com/token',
                authorization_response=authorization_response)

        # Guarda el token para futuras ejecuciones
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    # Usamos las credenciales para crear el servicio de la API de YouTube
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Ahora puedes utilizar la API de YouTube, como cambiar el título de un video
    youtube.videos().update(
        part="snippet",
        body=dict(
            id=video_id,
            snippet=dict(
                title=f"Nuevo título {viewCount} views"
            )
        )
    ).execute()

    print(f"Video {video_id} actualizado con éxito")

