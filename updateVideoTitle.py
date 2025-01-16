import google_auth_oauthlib.flow
import googleapiclient.discovery
import os

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
    if c.credentials:
        credentials = c.credentials
    else:
        # Print the URL for manual authorization
        auth_url, _ = flow.authorization_url(prompt='consent')
        print("Go to the following URL to authorize the application:")
        print(auth_url)
        authorization_response = input("Enter the authorization code: ")
        credentials = flow.fetch_token(
            'https://oauth2.googleapis.com/token',
            authorization_response=authorization_response)
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
                "description": desc,
                "title": title
            },
        }
    )
    response = request.execute()
    # print(response)
