import socket
import os
import struct

HOST = "0.0.0.0"
PORT = 12345
BUFFER_SIZE = 8192


def recibir_exactamente(sock, cantidad):
    datos = b""
    while len(datos) < cantidad:
        bloque = sock.recv(cantidad - len(datos))
        if not bloque:
            return None
        datos += bloque
    return datos


def recibir_utf(sock):
    longitud_bytes = recibir_exactamente(sock, 2)
    if not longitud_bytes:
        raise ConnectionError("No se pudo leer el nombre del archivo.")
    longitud = struct.unpack(">H", longitud_bytes)[0]
    return recibir_exactamente(sock, longitud).decode("utf-8")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen(1)

        print(f"Servidor listo en puerto {PORT}. Esperando UN cliente...")
        cliente, direccion = servidor.accept()
        print("Cliente conectado:", direccion)

        with cliente:
            file_name = recibir_utf(cliente)
            file_size = struct.unpack(">Q", recibir_exactamente(cliente, 8))[0]

            salida = "received_" + os.path.basename(file_name)
            total = 0

            print(f"Recibiendo archivo grande: {file_name} ({file_size} bytes)")

            with open(salida, "wb") as f:
                while total < file_size:
                    bloque = cliente.recv(min(BUFFER_SIZE, file_size - total))
                    if not bloque:
                        break
                    f.write(bloque)
                    total += len(bloque)

            print(f"Recepción completada: {salida}")
            print(f"Bytes recibidos: {total}/{file_size}")


if __name__ == "__main__":
    main()
