import socket
import os
import hashlib

HOST = "localhost"   # Cambia por la IP del servidor si estás en labmovil/nube
PORT = 12345
FILE_PATH = "uno.mp4"
BUFFER_SIZE = 8192


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(BUFFER_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def send_line(sock, text):
    sock.sendall((text + "\n").encode("utf-8"))


def receive_line(sock):
    data = b""
    while True:
        ch = sock.recv(1)
        if not ch or ch == b"\n":
            break
        data += ch
    return data.decode("utf-8")


def main():
    if not os.path.exists(FILE_PATH):
        print("No existe el archivo:", os.path.abspath(FILE_PATH))
        return

    file_name = os.path.basename(FILE_PATH)
    file_size = os.path.getsize(FILE_PATH)
    file_hash = sha256_file(FILE_PATH)

    print("Archivo:", file_name)
    print("Tamaño:", file_size, "bytes")
    print("SHA-256 local:", file_hash)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        send_line(client, file_name)
        send_line(client, str(file_size))
        send_line(client, file_hash)

        total_sent = 0
        last_percent = -1

        with open(FILE_PATH, "rb") as f:
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break

                client.sendall(chunk)
                total_sent += len(chunk)

                percent = int((total_sent * 100) / file_size)
                if percent != last_percent:
                    print(f"\rProgreso envío: {percent}%", end="")
                    last_percent = percent

        print("\nArchivo enviado. Esperando validación del servidor...")
        print("Respuesta del servidor:", receive_line(client))


if __name__ == "__main__":
    main()
