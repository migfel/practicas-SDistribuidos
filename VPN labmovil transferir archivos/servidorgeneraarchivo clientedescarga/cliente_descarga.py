import socket
import os
import time

HOST = "10.86.16.214"  # Cambiar por la IP del servidor
PORT = 5000

CARPETA_DESTINO = "descargas_cliente"
os.makedirs(CARPETA_DESTINO, exist_ok=True)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inicio = time.time()

cliente.connect((HOST, PORT))

nombre_archivo = cliente.recv(1024).decode()
cliente.sendall(b"OK_NOMBRE")

tamano_archivo = int(cliente.recv(1024).decode())
cliente.sendall(b"OK_TAMANO")

ruta_destino = os.path.join(CARPETA_DESTINO, nombre_archivo)

recibido = 0

with open(ruta_destino, "wb") as archivo:
    while recibido < tamano_archivo:
        datos = cliente.recv(4096)
        if not datos:
            break
        archivo.write(datos)
        recibido += len(datos)

cliente.close()

fin = time.time()
tiempo = fin - inicio
velocidad = (recibido / 1024 / 1024) / tiempo

print("Descarga finalizada")
print(f"Archivo recibido: {ruta_destino}")
print(f"Tamaño recibido: {recibido} bytes")
print(f"Tiempo total: {tiempo:.2f} segundos")
print(f"Velocidad aproximada: {velocidad:.2f} MB/s")