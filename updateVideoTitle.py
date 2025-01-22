import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def changeVideoTitle(viewCount, id, c):
    title = "Este vídeo tiene " + str(viewCount) + " Visitas"
    desc = "¿Estás impresionado?"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    flow = c.flow if c.flow else google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    c.flow = flow

    try:
        credentials = c.credentials if c.credentials else flow.run_local_server(port=8080)
        c.credentials = credentials
    except Exception as e:
        print(f"Error al intentar autorizar desde la consola: {e}")
        return

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

    print("Video actualizado con éxito:", response)

def main():
    viewCount = 137
    video_id = "7lqYwKU3WM4"
    
    c = type('', (), {})()
    c.credentials = None
    c.flow = None
    c.youtube = None

    changeVideoTitle(viewCount, video_id, c)

if __name__ == "__main__":
    main()
