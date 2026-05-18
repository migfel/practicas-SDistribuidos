import socket
import threading
import struct

HOST = "0.0.0.0"
PORT = 12345


def recibir_exactamente(sock, cantidad):
    datos = b""

    while len(datos) < cantidad:
        bloque = sock.recv(cantidad - len(datos))

        if not bloque:
            return None

        datos += bloque

    return datos


def recibir_utf(sock):
    longitud = recibir_exactamente(sock, 2)

    if not longitud:
        return None

    longitud = struct.unpack(">H", longitud)[0]

    datos = recibir_exactamente(sock, longitud)

    return datos.decode("utf-8")


def manejar_cliente(cliente, direccion):
    try:
        # 1. Leer nombre del archivo
        file_name = recibir_utf(cliente)

        # 2. Leer tamaño del archivo
        size_bytes = recibir_exactamente(cliente, 8)

        file_size = struct.unpack(">Q", size_bytes)[0]

        salida = open("received_" + file_name, "wb")

        buffer_size = 8192
        total_read = 0
        last_percent = 0

        print(f"Recibiendo archivo: {file_name} ({file_size} bytes)")

        # 3. Leer exactamente file_size bytes
        while total_read < file_size:

            faltante = file_size - total_read

            datos = cliente.recv(min(buffer_size, faltante))

            if not datos:
                break

            salida.write(datos)

            total_read += len(datos)

            percent = int((total_read * 100) / file_size)

            if percent != last_percent:
                print(f"\rProgreso recepción: {percent}%", end="")
                last_percent = percent

        print(f"\nRecepción completada de: {file_name}")

        salida.close()
        cliente.close()

    except Exception as e:
        print("Error:")
        print(e)


try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST, PORT))

    servidor.listen()

    print(f"Servidor listo en puerto {PORT}...")

    while True:
        cliente, direccion = servidor.accept()

        print(f"Cliente conectado: {direccion}")

        hilo = threading.Thread(
            target=manejar_cliente,
            args=(cliente, direccion)
        )

        hilo.start()

except Exception as e:
    print("Error:")
    print(e)
