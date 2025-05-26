import requests

url = "http://localhost:5000/hola?nombre=Luis"

respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()
    print("Respuesta GET:", datos["mensaje"])
else:
    print("Error al contactar el servidor:", respuesta.status_code)
