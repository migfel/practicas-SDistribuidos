import socket
import os
import time

HOST = "10.86.16.214"  # Cambiar por la IP del servidor
PORT = 5000

NOMBRE_ARCHIVO = "archivo_grande_cliente.bin"
TAMANO_MB = 100

print("Generando archivo grande...")

with open(NOMBRE_ARCHIVO, "wb") as archivo:
    archivo.write(os.urandom(TAMANO_MB * 1024 * 1024))

tamano_archivo = os.path.getsize(NOMBRE_ARCHIVO)

print(f"Archivo generado: {NOMBRE_ARCHIVO}")
print(f"Tamaño: {tamano_archivo} bytes")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inicio = time.time()

cliente.connect((HOST, PORT))

cliente.sendall(NOMBRE_ARCHIVO.encode())
cliente.recv(1024)

cliente.sendall(str(tamano_archivo).encode())
cliente.recv(1024)

with open(NOMBRE_ARCHIVO, "rb") as archivo:
    while True:
        datos = archivo.read(4096)
        if not datos:
            break
        cliente.sendall(datos)

cliente.close()

fin = time.time()
tiempo = fin - inicio
velocidad = (TAMANO_MB / tiempo)

print("Transferencia finalizada")
print(f"Tiempo total: {tiempo:.2f} segundos")
print(f"Velocidad aproximada: {velocidad:.2f} MB/s")