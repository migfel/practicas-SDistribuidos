import tkinter as tk
import requests

def consultar_api():
    nombre = entry_nombre.get()
    url = f"http://localhost:5000/hola?nombre={nombre}"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            label_resultado.config(text=datos["mensaje"])
        else:
            label_resultado.config(text=f"Error: {respuesta.status_code}")
    except Exception as e:
        label_resultado.config(text=f"Error de conexión: {e}")

root = tk.Tk()
root.title("Cliente GUI para Hola Mundo")

tk.Label(root, text="Ingresa tu nombre:").pack(pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.pack(pady=5)

boton = tk.Button(root, text="Enviar", command=consultar_api)
boton.pack(pady=10)

label_resultado = tk.Label(root, text="")
label_resultado.pack(pady=10)

root.mainloop()
