import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "TU_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def buscar():
    ciudad = entrada.get().strip()

    if not ciudad:
        messagebox.showwarning("Aviso", "Escribe una ciudad")
        return

    params = {
        "q": ciudad,
        "units": "metric",
        "appid": API_KEY,
        "lang": "es"
    }

    try:
        respuesta = requests.get(BASE_URL, params=params, timeout=10)
        data = respuesta.json()

        if data.get("cod") != 200:
            resultado.config(text="Error: " + str(data.get("message")))
            return

        resultado.config(
            text=f"Ciudad: {data['name']}\n"
                 f"Temperatura: {data['main']['temp']} °C\n"
                 f"Humedad: {data['main']['humidity']}%\n"
                 f"Clima: {data['weather'][0]['description']}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

ventana = tk.Tk()
ventana.title("Consulta de Clima")

tk.Label(ventana, text="Ciudad:").pack(pady=5)

entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=5)

tk.Button(ventana, text="Consultar", command=buscar).pack(pady=10)

resultado = tk.Label(ventana, text="", justify="left")
resultado.pack(pady=10)

ventana.mainloop()