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
    longitud = struct.unpack(">H", longitud)[0]

    datos = recibir_exactamente(sock, longitud)

    return datos.decode("utf-8")


def manejar_cliente(cliente, direccion):
    try:
        print(f"Cliente conectado: {direccion}")

        # 1. Leer nombre del archivo
        nombre_archivo = recibir_utf(cliente)

        # 2. Leer tamaño
        tamano_bytes = recibir_exactamente(cliente, 8)
        tamano_archivo = struct.unpack(">Q", tamano_bytes)[0]

        tamano_mb = tamano_archivo / (1024 * 1024)

        print(f"Recibiendo archivo: {nombre_archivo} ({tamano_mb:.2f} MB)")

        salida = open("received_" + nombre_archivo, "wb")

        total_recibido = 0
        ultimo_porcentaje = -1

        # 3. Recibir contenido
        while total_recibido < tamano_archivo:
            faltante = tamano_archivo - total_recibido

            datos = cliente.recv(min(8192, faltante))

            if not datos:
                break

            salida.write(datos)

            total_recibido += len(datos)

            porcentaje = int((total_recibido * 100) / tamano_archivo)
            recibidos_mb = total_recibido / (1024 * 1024)

            if porcentaje != ultimo_porcentaje:
                print(
                    f"\rProgreso recepción: {porcentaje:3d}% "
                    f"({recibidos_mb:.2f} / {tamano_mb:.2f} MB)",
                    end=""
                )

                ultimo_porcentaje = porcentaje

        print(f"\nRecepción completada de: {nombre_archivo}")

        salida.close()
        cliente.close()

    except Exception as e:
        print("Error:")
        print(e)


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servidor.bind((HOST, PORT))
servidor.listen()

print("Servidor listo en puerto 12345...")

while True:
    cliente, direccion = servidor.accept()

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente, direccion)
    )

    hilo.start()
