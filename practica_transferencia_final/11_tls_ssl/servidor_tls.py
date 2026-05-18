import socket
import ssl
import os

HOST = "0.0.0.0"
PORT = 12345
BUFFER_SIZE = 8192
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"


def receive_line(sock):
    data = b""
    while True:
        ch = sock.recv(1)
        if not ch or ch == b"\n":
            break
        data += ch
    return data.decode("utf-8")


def main():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("Faltan cert.pem y key.pem.")
        print("Genera los certificados con:")
        print("openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes")
        return

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw_server:
        raw_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw_server.bind((HOST, PORT))
        raw_server.listen(5)

        print(f"Servidor TLS listo en puerto {PORT}...")
        raw_client, address = raw_server.accept()
        print("Cliente conectado:", address)

        with context.wrap_socket(raw_client, server_side=True) as client:
            file_name = receive_line(client)
            file_size = int(receive_line(client))

            output_name = "tls_received_" + os.path.basename(file_name)
            total_read = 0
            last_percent = -1

            print(f"Recibiendo con TLS: {file_name} ({file_size} bytes)")

            with open(output_name, "wb") as out:
                while total_read < file_size:
                    chunk = client.recv(min(BUFFER_SIZE, file_size - total_read))
                    if not chunk:
                        break
                    out.write(chunk)
                    total_read += len(chunk)

                    percent = int((total_read * 100) / file_size)
                    if percent != last_percent:
                        print(f"\rProgreso TLS recepción: {percent}%", end="")
                        last_percent = percent

            print(f"\nRecepción TLS completada: {output_name}")


if __name__ == "__main__":
    main()
