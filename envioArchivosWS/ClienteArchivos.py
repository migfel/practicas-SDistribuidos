import requests

filename = "mi_archivo.txt"
url = f"http://127.0.0.1:5000/download/{filename}"

response = requests.get(url)

if response.status_code == 200:
    with open(f"descargado_{filename}", 'wb') as f:
        f.write(response.content)
    print(f"Archivo descargado y guardado como descargado_{filename}")
else:
    print("Error al descargar el archivo:", response.json())
