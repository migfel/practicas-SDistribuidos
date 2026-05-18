import socket
import struct
import os

HOST = "localhost"
PORT = 12345
ARCHIVO = "uno.mp4"


def enviar_utf(sock, texto):
    datos = texto.encode("utf-8")
    sock.sendall(struct.pack(">H", len(datos)))
    sock.sendall(datos)


try:
    archivo = ARCHIVO

    if not os.path.exists(archivo):
        print("El archivo no existe.")
        exit()

    tamano_archivo = os.path.getsize(archivo)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    # 1. Enviar nombre
    enviar_utf(cliente, os.path.basename(archivo))

    # 2. Enviar tamaño
    cliente.sendall(struct.pack(">Q", tamano_archivo))

    # 3. Enviar contenido
    total_enviado = 0
    ultimo_porcentaje = -1
    tamano_mb = tamano_archivo / (1024 * 1024)

    print(f"Enviando archivo: {archivo} ({tamano_mb:.2f} MB)")

    with open(archivo, "rb") as f:
        while True:
            datos = f.read(8192)

            if not datos:
                break

            cliente.sendall(datos)

            total_enviado += len(datos)

            porcentaje = int((total_enviado * 100) / tamano_archivo)
            enviados_mb = total_enviado / (1024 * 1024)

            if porcentaje != ultimo_porcentaje:
                print(
                    f"\rProgreso envío: {porcentaje:3d}% "
                    f"({enviados_mb:.2f} / {tamano_mb:.2f} MB)",
                    end=""
                )

                ultimo_porcentaje = porcentaje

    print("\nEnvío completado.")

    cliente.close()

except Exception as e:
    print("Error:")
    print(e)
