import socket
import os
import hashlib
import threading

HOST = "0.0.0.0"
PORT = 12345
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


def handle_client(client, address):
    try:
        print("Cliente conectado:", address)

        with client:
            file_name = receive_line(client)
            file_size = int(receive_line(client))
            expected_hash = receive_line(client)

            output_name = "received_" + os.path.basename(file_name)
            total_read = 0
            last_percent = -1

            print(f"Recibiendo archivo: {file_name} ({file_size} bytes)")
            print("SHA-256 esperado:", expected_hash)

            with open(output_name, "wb") as out:
                while total_read < file_size:
                    chunk = client.recv(min(BUFFER_SIZE, file_size - total_read))
                    if not chunk:
                        break
                    out.write(chunk)
                    total_read += len(chunk)

                    percent = int((total_read * 100) / file_size)
                    if percent != last_percent:
                        print(f"\rProgreso recepción: {percent}%", end="")
                        last_percent = percent

            received_hash = sha256_file(output_name)

            print("\nSHA-256 recibido:", received_hash)

            if expected_hash == received_hash:
                message = "OK: integridad verificada con SHA-256."
            else:
                message = "ERROR: el hash no coincide. Archivo corrupto o incompleto."

            print(message)
            send_line(client, message)

    except Exception as e:
        print("Error atendiendo cliente:", e)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(10)

        print(f"Servidor SHA-256 multicliente listo en puerto {PORT}...")

        while True:
            client, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client, address), daemon=True)
            thread.start()


if __name__ == "__main__":
    main()
