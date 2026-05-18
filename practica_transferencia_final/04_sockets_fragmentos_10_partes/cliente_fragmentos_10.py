import socket
import struct

HOST = "localhost"
PORT = 12345
ARCHIVO = "example.bin"


def enviar_utf(sock, texto):
    datos = texto.encode("utf-8")
    sock.sendall(struct.pack(">H", len(datos)))
    sock.sendall(datos)


try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    # Enviar nombre del archivo
    enviar_utf(cliente, "example.bin")

    # Enviar archivo en 10 fragmentos
    with open(ARCHIVO, "rb") as archivo:
        buffer_size = 1024

        for i in range(10):
            datos = archivo.read(buffer_size)

            if not datos:
                break

            cliente.sendall(datos)

    print("Archivo enviado correctamente.")

    cliente.close()

except Exception as e:
    print("Error:")
    print(e)
