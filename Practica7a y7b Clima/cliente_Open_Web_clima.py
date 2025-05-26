# cliente_clima.py
import urllib.request
import json

def obtener_datos_clima(base_url, ciudad_id, api_key=None):
    if "openweathermap" in base_url:
        url = f"{base_url}?id={ciudad_id}&units=metric&APPID={api_key}&lang=en"
    else:
        # Si es servidor local, no necesita API Key ni parámetros
        url = f"{base_url}"

    print(f"Consultando: {url}")
    try:
        respuesta = urllib.request.urlopen(url, timeout=30)
        datos = json.loads(respuesta.read())
        print("Ciudad:", datos["name"])
        print("Temperatura:", datos["main"]["temp"], "°C")
        print("Clima:", datos["weather"][0]["main"])
    except Exception as e:
        print("Error al obtener datos:", e)

# Cambia esta variable para usar OpenWeather o tu servidor local
# --- OPCIÓN A: Servidor real (requiere tu API Key)
#base_url = "http://api.openweathermap.org/data/2.5/weather"
#ciudad_id = "3530597"  # ID de CDMX
#api_key = "TU_API_KEY"

# --- OPCIÓN B: Servidor simulado (localhost)
base_url = "http://localhost:8080/data/2.5/weather"
ciudad_id = None
api_key = None

obtener_datos_clima(base_url, ciudad_id, api_key)

# --- OPCIÓN :C Servidor en Flask
