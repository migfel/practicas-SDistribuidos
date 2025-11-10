import requests
import tkinter as tk
from tkinter import filedialog

# Función para cargar un archivo al servidor
def cargar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    ruta_archivo = filedialog.askopenfilename()  # Abre un cuadro de diálogo para seleccionar un archivo
    if ruta_archivo:
        url = 'http://localhost:5000/upload'
        archivos = {'file': open(ruta_archivo, 'rb')}
        respuesta = requests.post(url, files=archivos)
        print(respuesta.json())

# Función para descargar un archivo desde el servidor
def descargar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    ruta_archivo = filedialog.asksaveasfilename()  # Abre un cuadro de diálogo para seleccionar una ubicación de descarga
    if ruta_archivo:
        url = 'http://localhost:5000/descargar/archivo.txt'  # Debes especificar el nombre del archivo que deseas descargar
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            with open(ruta_archivo, 'wb') as f:
                f.write(respuesta.content)
            print(f'Archivo descargado en "{ruta_archivo}"')

if __name__ == '__main__':
    print("1. Cargar Archivo")
    print("2. Descargar Archivo")

    eleccion = input("Ingresa tu elección (1/2): ")

    if eleccion == '1':
        cargar_archivo()
    elif eleccion == '2':
        descargar_archivo()
    else:
        print("Elección no válida")

