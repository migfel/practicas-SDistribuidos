import socket
import struct
import os
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = 12345
FILE_PATH = "uno.mp4"


def enviar_utf(sock, texto):
    datos = texto.encode("utf-8")

    # Equivalente a writeUTF de Java
    sock.sendall(struct.pack(">H", len(datos)))
    sock.sendall(datos)


try:
    # Archivo a enviar
    if not os.path.exists(FILE_PATH):
        print("El archivo no existe:", os.path.abspath(FILE_PATH))
        exit()

    file_size = os.path.getsize(FILE_PATH)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    # 1. Enviar nombre del archivo
    enviar_utf(cliente, os.path.basename(FILE_PATH))

    # 2. Enviar tamaño del archivo
    cliente.sendall(struct.pack(">Q", file_size))

    # 3. Enviar contenido
    buffer_size = 8192
    total_sent = 0
    last_percent = 0

    print(f"Enviando archivo: {os.path.basename(FILE_PATH)} ({file_size} bytes)")

    with open(FILE_PATH, "rb") as archivo:

        while True:
            datos = archivo.read(buffer_size)

            if not datos:
                break

            cliente.sendall(datos)

            total_sent += len(datos)

            percent = int((total_sent * 100) / file_size)

            if percent != last_percent:
                print(f"\rProgreso envío: {percent}%", end="")
                last_percent = percent

    print("\nEnvío completado.")

    cliente.close()

except Exception as e:
    print("Error:")
    print(e)
