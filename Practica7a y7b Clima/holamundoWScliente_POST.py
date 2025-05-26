import requests

url = "http://localhost:5000/hola"
datos = {"nombre": "Luis"}

respuesta = requests.post(url, json=datos)

if respuesta.status_code == 200:
    print("Respuesta POST:", respuesta.json()["mensaje"])
else:
    print("Error:", respuesta.status_code)
