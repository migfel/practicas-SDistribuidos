#!/usr/bin/env python3
import requests

API_KEY = "TU_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def obtener_clima(ciudad):
    params = {
        "q": ciudad,
        "units": "metric",
        "appid": API_KEY,
        "lang": "es"
    }

    try:
        respuesta = requests.get(BASE_URL, params=params, timeout=10)
        respuesta.raise_for_status()

        data = respuesta.json()

        if data.get("cod") != 200:
            return {"error": data.get("message")}

        return {
            "ciudad": data["name"],
            "temperatura": data["main"]["temp"],
            "humedad": data["main"]["humidity"],
            "clima": data["weather"][0]["description"]
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    ciudad = input("Escribe el nombre de la ciudad: ")

    resultado = obtener_clima(ciudad)

    if "error" in resultado:
        print("Error:", resultado["error"])
    else:
        print("\nResultado:")
        print("Ciudad:", resultado["ciudad"])
        print("Temperatura:", resultado["temperatura"], "°C")
        print("Humedad:", resultado["humedad"], "%")
        print("Clima:", resultado["clima"])