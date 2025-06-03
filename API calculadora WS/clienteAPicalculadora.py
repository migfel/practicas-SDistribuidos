import requests

# Cambia esto según la operación
operacion = 'multiplicar'  # sumar, restar, multiplicar, dividir
a = 12
b = 3

url = f'http://localhost:5000/calculadora/{operacion}'
params = {'a': a, 'b': b}
resp = requests.get(url, params=params)

print(resp.json())
