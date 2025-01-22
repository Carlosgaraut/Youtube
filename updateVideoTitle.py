import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import time

class creds:
    def __init__(self):
        self.credentials = False
        self.flow = False
        self.youtube = False
        self.viewCount = 0
        self.num = 0

def changeVideoTitle(viewCount, id, c):
    title = "Este vídeo tiene " + str(viewCount) + " Visitas"
    desc = "¿Estás impresionado?"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

    # Desactivar la verificación HTTPS solo para entorno local
    # *NO DEJES ESTA OPCIÓN ACTIVADA EN PRODUCCIÓN*
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"  # Asegúrate de tener este archivo en tu directorio

    # Obtener credenciales y crear un cliente de la API
    flow = c.flow if c.flow else google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    c.flow = flow

    try:
        # Intentamos usar el flujo local sin abrir el navegador
        credentials = c.credentials if c.credentials else flow.run_local_server(port=8888)
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


def getViews(VID_ID, API_KEY):
    import urllib.request
    import json

    url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=' + VID_ID + '&key=' + API_KEY
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    res = json.loads(respData.decode('utf-8'))
    statistics = res["items"][0]["statistics"]
    viewCount = statistics["viewCount"]
    return viewCount


def main():
    c = creds()
    timeout = 720  # Tiempo por defecto en segundos (12 minutos)
    
    # Bucle de 20,000 ejecuciones
    while c.num < 20000:
        id = "7lqYwKU3WM4"  # ID del video
        API_KEY = "TU_API_KEY_AQUI"  # Reemplaza esto con tu API Key de YouTube

        # Obtiene el número de vistas del video
        viewCount = int(getViews(id, API_KEY))

        # Verifica si el número de vistas ha cambiado
        if viewCount != c.viewCount:
            changeVideoTitle(viewCount, id, c)
            print("Changing viewCount...")
            print("Go to https://www.youtube.com/watch?v=" + str(id) + " and check out the name.")
            timeout = 480  # Si cambia el contador de vistas, el tiempo de espera será de 8 minutos
        else:
            print("The view count is the same as it was so we are not changing")
            timeout = 240  # Si no cambia, el tiempo de espera será de 4 minutos

        c.viewCount = viewCount  # Actualiza el contador de vistas

        # Espera durante el tiempo especificado (timeout)
        for i in range(timeout):
            time.sleep(1)
            if (timeout - i) % 60 == 0:  # Imprime los minutos restantes
                print(f"Time remaining: {timeout-i} seconds")
        
        print(f"Completed running time number {c.num}.")
        c.num += 1  # Incrementa el contador de ejecuciones


if __name__ == "__main__":
    main()
