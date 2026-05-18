import socket
import threading
import struct

HOST = "0.0.0.0"
PORT = 12345
BUFFER_SIZE = 4096


def recibir_utf(sock):
    """
    Equivalente aproximado a readUTF de Java:
    lee primero 2 bytes con la longitud y luego lee el texto en UTF-8.
    """
    longitud_bytes = recibir_exactamente(sock, 2)
    if not longitud_bytes:
        raise ConnectionError("No se pudo leer la longitud del nombre del archivo.")

    longitud = struct.unpack(">H", longitud_bytes)[0]
    datos = recibir_exactamente(sock, longitud)

    if not datos:
        raise ConnectionError("No se pudo leer el nombre del archivo.")

    return datos.decode("utf-8")


def recibir_exactamente(sock, cantidad):
    """
    Recibe exactamente la cantidad de bytes indicada.
    """
    datos = b""

    while len(datos) < cantidad:
        bloque = sock.recv(cantidad - len(datos))
        if not bloque:
            return None
        datos += bloque

    return datos


def atender_cliente(cliente, direccion):
    try:
        with cliente:
            nombre_archivo = recibir_utf(cliente)

            # Recibir tamaño del archivo como long de Java: 8 bytes, big-endian
            tamano_bytes = recibir_exactamente(cliente, 8)
            if not tamano_bytes:
                raise ConnectionError("No se pudo leer el tamaño del archivo.")

            tamano_archivo = struct.unpack(">Q", tamano_bytes)[0]

            nombre_salida = "received_" + nombre_archivo
            total_leido = 0

            with open(nombre_salida, "wb") as archivo_salida:
                # Recibir exactamente tamano_archivo bytes
                while total_leido < tamano_archivo:
                    faltante = tamano_archivo - total_leido
                    bloque = cliente.recv(min(BUFFER_SIZE, faltante))

                    if not bloque:
                        break

                    archivo_salida.write(bloque)
                    total_leido += len(bloque)

            print(f"Archivo {nombre_archivo} recibido correctamente desde {direccion}.")

    except Exception as e:
        print(f"Error atendiendo al cliente {direccion}:")
        print(e)


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((HOST, PORT))
            servidor.listen()

            print("Servidor listo...")

            while True:
                cliente, direccion = servidor.accept()
                hilo = threading.Thread(
                    target=atender_cliente,
                    args=(cliente, direccion),
                    daemon=True
                )
                hilo.start()

    except Exception as e:
        print("Error en el servidor:")
        print(e)


if __name__ == "__main__":
    main()
