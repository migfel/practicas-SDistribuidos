import requests

def obtener_clima(ciudad_id):
    url = "http://127.0.0.1:5000/clima"
    params = {"id": ciudad_id}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        datos = response.json()
        if datos.get("cod") == 200:
            print(f"Ciudad: {datos['name']}")
            print(f"Temperatura: {datos['main']['temp']}°C")
            print(f"Clima: {datos['weather'][0]['main']}")
        else:
            print(f"Error: {datos.get('message', 'Error desconocido')}")
    else:
        print(f"Error en la conexión: {response.status_code}")

if __name__ == "__main__":
    print("Consulta de Clima")
    ciudad_id = input("Ingresa el ID de la ciudad (3995465 para Monterrey, 3530597 para CDMX): ")
    obtener_clima(ciudad_id)
