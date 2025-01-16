from updateVideoTitle import changeVideoTitle
from videoDetailsRequest import getViews
import time


class creds:
    def __init__(self):
        self.credentials = False
        self.flow = False
        self.youtube = False
        self.viewCount = 0
        self.num = 0


def main():
    c = creds()
    timeout = 720  # Tiempo por defecto en segundos (12 minutos)
    
    # Bucle de 20,000 ejecuciones
    while c.num < 20000:  # Corrigiendo la coma
        id = "7lqYwKU3WM4"
        API_KEY = "AIzaSyA5VygQ4sTuR0UwQG-ninp-6lkND2Dmrlw"
        
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
