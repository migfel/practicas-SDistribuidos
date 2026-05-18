import socket

def main():
    HOST = "0.0.0.0"
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print("Servidor esperando conexión...")

    client_socket, addr = server_socket.accept()
    print(f"Cliente conectado desde: {addr}")

    # Recibir nombre del archivo
    filename_length = int.from_bytes(client_socket.recv(4), "big")
    filename = client_socket.recv(filename_length).decode()
    print(f"Nombre del archivo recibido: {filename}")

    # Preparar archivo destino
    with open(filename, "wb") as f:
        while True:
            chunk_size_bytes = client_socket.recv(4)
            if not chunk_size_bytes:
                break  # No más datos

            chunk_size = int.from_bytes(chunk_size_bytes, "big")
            if chunk_size == 0:
                break  # Fin del archivo

            data = client_socket.recv(chunk_size)
            f.write(data)

    print("Archivo recibido correctamente.")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
