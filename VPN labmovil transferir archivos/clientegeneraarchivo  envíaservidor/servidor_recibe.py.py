import socket
import os

HOST = "0.0.0.0"
PORT = 5000
CARPETA_DESTINO = "archivos_recibidos"

os.makedirs(CARPETA_DESTINO, exist_ok=True)

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen(5)

print(f"Servidor escuchando en puerto {PORT}...")

while True:
    conexion, direccion = servidor.accept()
    print(f"Conexión recibida desde {direccion}")

    nombre_archivo = conexion.recv(1024).decode()
    conexion.sendall(b"OK_NOMBRE")

    tamano_archivo = int(conexion.recv(1024).decode())
    conexion.sendall(b"OK_TAMANO")

    ruta_destino = os.path.join(CARPETA_DESTINO, nombre_archivo)

    recibido = 0

    with open(ruta_destino, "wb") as archivo:
        while recibido < tamano_archivo:
            datos = conexion.recv(4096)
            if not datos:
                break
            archivo.write(datos)
            recibido += len(datos)

    print(f"Archivo recibido: {ruta_destino}")
    print(f"Tamaño recibido: {recibido} bytes")

    conexion.close()