import socket
import ssl
import os

HOST = "localhost"   # Cambia por la IP del servidor si estás en labmovil/nube
PORT = 12345
FILE_PATH = "uno.mp4"
BUFFER_SIZE = 8192


def send_line(sock, text):
    sock.sendall((text + "\n").encode("utf-8"))


def main():
    if not os.path.exists(FILE_PATH):
        print("No existe el archivo:", os.path.abspath(FILE_PATH))
        return

    file_name = os.path.basename(FILE_PATH)
    file_size = os.path.getsize(FILE_PATH)

    # En laboratorio usamos certificado autofirmado, por eso no se verifica CA.
    context = ssl._create_unverified_context()
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with context.wrap_socket(raw_socket, server_hostname=HOST) as client:
        client.connect((HOST, PORT))

        send_line(client, file_name)
        send_line(client, str(file_size))

        total_sent = 0
        last_percent = -1

        print(f"Enviando con TLS: {file_name} ({file_size} bytes)")

        with open(FILE_PATH, "rb") as f:
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break

                client.sendall(chunk)
                total_sent += len(chunk)

                percent = int((total_sent * 100) / file_size)
                if percent != last_percent:
                    print(f"\rProgreso TLS envío: {percent}%", end="")
                    last_percent = percent

    print("\nEnvío TLS completado.")


if __name__ == "__main__":
    main()
