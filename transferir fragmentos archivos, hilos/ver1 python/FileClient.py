import socket
import os

def main():
    SERVER = "localhost"
    PORT = 12345
    FILE_PATH = "example.bin"   # Cambia la ruta si lo necesitas

    if not os.path.exists(FILE_PATH):
        print("El archivo no existe:", FILE_PATH)
        return

    # Conectarse al servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))
    print("Conectado al servidor.")

    # Enviar nombre del archivo
    filename = os.path.basename(FILE_PATH).encode()
    client_socket.send(len(filename).to_bytes(4, "big"))
    client_socket.send(filename)

    # Enviar archivo en partes (chunks)
    with open(FILE_PATH, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            client_socket.send(len(chunk).to_bytes(4, "big"))
            client_socket.send(chunk)

    # Enviar chunk final vacío (fin del archivo)
    client_socket.send((0).to_bytes(4, "big"))

    print("Archivo enviado exitosamente.")
    client_socket.close()

if __name__ == "__main__":
    main()
