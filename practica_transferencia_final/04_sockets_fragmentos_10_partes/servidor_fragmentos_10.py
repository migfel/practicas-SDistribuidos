import socket
import threading
import struct


HOST = "0.0.0.0"
PORT = 12345


def recibir_utf(sock):
    longitud = sock.recv(2)
    longitud = struct.unpack(">H", longitud)[0]

    datos = sock.recv(longitud)

    return datos.decode("utf-8")


def manejar_cliente(cliente):
    try:
        # Leer nombre del archivo
        nombre_archivo = recibir_utf(cliente)

        print(f"Recibiendo archivo: {nombre_archivo}")

        # Crear archivo de salida
        salida = open("received_" + nombre_archivo, "wb")

        # Recibir archivo en 10 fragmentos
        buffer_size = 1024

        for i in range(10):
            datos = cliente.recv(buffer_size)

            if not datos:
                break

            salida.write(datos)

        print("Archivo recibido correctamente.")

        salida.close()
        cliente.close()

    except Exception as e:
        print("Error:")
        print(e)


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print("Servidor listo...")

while True:
    cliente, direccion = servidor.accept()

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente,)
    )

    hilo.start()
