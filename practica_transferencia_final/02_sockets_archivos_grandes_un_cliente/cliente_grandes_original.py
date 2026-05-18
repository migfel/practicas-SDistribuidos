import socket
import os
import struct

HOST = "localhost"
PORT = 12345
FILE_PATH = "uno.mp4"
BUFFER_SIZE = 4096


def enviar_utf(sock, texto):
    """
    Equivalente aproximado a writeUTF de Java:
    primero envía la longitud del texto en 2 bytes y luego el texto en UTF-8.
    """
    datos = texto.encode("utf-8")
    sock.sendall(struct.pack(">H", len(datos)))
    sock.sendall(datos)


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PORT))

            nombre_archivo = os.path.basename(FILE_PATH)
            tamano_archivo = os.path.getsize(FILE_PATH)

            # 1. Enviar nombre del archivo
            enviar_utf(cliente, nombre_archivo)

            # 2. Enviar tamaño del archivo como long de Java: 8 bytes, big-endian
            cliente.sendall(struct.pack(">Q", tamano_archivo))

            # 3. Enviar contenido del archivo
            with open(FILE_PATH, "rb") as archivo:
                while True:
                    bloque = archivo.read(BUFFER_SIZE)
                    if not bloque:
                        break
                    cliente.sendall(bloque)

        print("Archivo enviado correctamente.")

    except Exception as e:
        print("Error al enviar el archivo:")
        print(e)


if __name__ == "__main__":
    main()
