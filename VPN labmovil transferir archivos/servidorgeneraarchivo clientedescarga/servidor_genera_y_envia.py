import socket
import os
import time

HOST = "0.0.0.0"
PORT = 5000

NOMBRE_ARCHIVO = "archivo_grande_servidor.bin"
TAMANO_MB = 100

print("Generando archivo grande en el servidor...")

with open(NOMBRE_ARCHIVO, "wb") as archivo:
    archivo.write(os.urandom(TAMANO_MB * 1024 * 1024))

tamano_archivo = os.path.getsize(NOMBRE_ARCHIVO)

print(f"Archivo generado: {NOMBRE_ARCHIVO}")
print(f"Tamaño: {tamano_archivo} bytes")

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen(5)

print(f"Servidor listo. Esperando clientes en puerto {PORT}...")

while True:
    conexion, direccion = servidor.accept()
    print(f"Cliente conectado desde {direccion}")

    inicio = time.time()

    conexion.sendall(NOMBRE_ARCHIVO.encode())
    conexion.recv(1024)

    conexion.sendall(str(tamano_archivo).encode())
    conexion.recv(1024)

    with open(NOMBRE_ARCHIVO, "rb") as archivo:
        while True:
            datos = archivo.read(4096)
            if not datos:
                break
            conexion.sendall(datos)

    conexion.close()

    fin = time.time()
    tiempo = fin - inicio
    velocidad = TAMANO_MB / tiempo

    print("Archivo enviado al cliente")
    print(f"Tiempo total: {tiempo:.2f} segundos")
    print(f"Velocidad aproximada: {velocidad:.2f} MB/s")