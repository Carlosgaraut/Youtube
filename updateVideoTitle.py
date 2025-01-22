import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def changeVideoTitle(viewCount, id, c):
    title = "Este vídeo tiene " + str(viewCount) + " Visitas"
    desc = "¿Estás impresionado?"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    # Desactivar la verificación HTTPS solo para entorno local
    # *NO DEJES ESTA OPCIÓN ACTIVADA EN PRODUCCIÓN*
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"  # Ruta de tu archivo de secretos

    # Obtener credenciales y crear un cliente de la API
    flow = c.flow if c.flow else google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    c.flow = flow

    # Asegúrate de usar la IP pública de tu instancia en Google Cloud
    flow.redirect_uri = 'http://104.154.249.111:8080/'  # Cambia por la IP pública de tu VM

    try:
        # Intentamos usar el flujo local sin abrir el navegador
        credentials = c.credentials if c.credentials else flow.run_local_server(port=8080)
        c.credentials = credentials
    except Exception as e:
        print(f"Error al intentar autorizar desde la consola: {e}")
        return

    # Crear el cliente de YouTube con las credenciales
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

    # Mostrar respuesta (puedes cambiar esto según lo que necesites)
    print("Video actualizado con éxito:", response)


# Aquí colocas el código para llamar a la función
def main():
    # Suponiendo que ya tienes el `viewCount` y `id` del video
    viewCount = 137  # Cambia este valor según tu caso
    video_id = "7lqYwKU3WM4"  # El ID de tu video en YouTube

    # Creamos el objeto 'c' donde guardamos las credenciales y el cliente
    c = type('', (), {})()  # Creamos un objeto vacío para 'c'
    c.credentials = None
    c.flow = None
    c.youtube = None

    changeVideoTitle(viewCount, video_id, c)

if __name__ == "__main__":
    main()
