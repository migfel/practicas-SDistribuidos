import socket
import os
import struct

HOST = "localhost"   # Cambia por la IP del servidor en labmovil/nube
PORT = 12345
FILE_PATH = "uno.mp4"
BUFFER_SIZE = 8192


def enviar_utf(sock, texto):
    datos = texto.encode("utf-8")
    sock.sendall(struct.pack(">H", len(datos)))
    sock.sendall(datos)


def main():
    if not os.path.exists(FILE_PATH):
        print("El archivo no existe:", os.path.abspath(FILE_PATH))
        return

    file_name = os.path.basename(FILE_PATH)
    file_size = os.path.getsize(FILE_PATH)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))

        enviar_utf(cliente, file_name)
        cliente.sendall(struct.pack(">Q", file_size))

        print(f"Enviando archivo grande: {file_name} ({file_size} bytes)")

        with open(FILE_PATH, "rb") as f:
            while True:
                bloque = f.read(BUFFER_SIZE)
                if not bloque:
                    break
                cliente.sendall(bloque)

    print("Archivo enviado correctamente.")


if __name__ == "__main__":
    main()
