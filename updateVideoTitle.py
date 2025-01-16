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

    # Disable opening the browser automatically
    credentials = c.credentials if c.credentials else flow.run_local_server(port=8080, open_browser=False)
    c.credentials = credentials

    youtube = c.youtube if c.youtube else googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    c.youtube = youtube

    # Once the flow is done, you can manually copy the URL printed in the logs and open it in your browser
    print(f"Open this URL in your browser and authorize the app: {flow.authorization_url()[0]}")

    # Update the video title
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
    # Uncomment to view the API response
    # print(response)
