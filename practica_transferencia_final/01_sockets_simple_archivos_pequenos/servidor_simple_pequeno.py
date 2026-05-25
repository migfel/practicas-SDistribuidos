import socket
import os

def recibir_exactamente(sock, n):
    datos = b""
    while len(datos) < n:
        parte = sock.recv(n - len(datos))
        if not parte:
            return None
        datos += parte
    return datos

def main():
    HOST = "0.0.0.0"
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print("Servidor esperando conexión...")

    client_socket, addr = server_socket.accept()
    print(f"Cliente conectado desde: {addr}")

    filename_length_bytes = recibir_exactamente(client_socket, 4)
    filename_length = int.from_bytes(filename_length_bytes, "big")

    filename_bytes = recibir_exactamente(client_socket, filename_length)
    filename = filename_bytes.decode()

    output_filename = "received_" + os.path.basename(filename)
    print(f"Nombre del archivo recibido: {filename}")

    total_recibido = 0

    with open(output_filename, "wb") as f:
        while True:
            chunk_size_bytes = recibir_exactamente(client_socket, 4)

            if not chunk_size_bytes:
                break

            chunk_size = int.from_bytes(chunk_size_bytes, "big")

            if chunk_size == 0:
                break

            data = recibir_exactamente(client_socket, chunk_size)

            if not data:
                break

            f.write(data)
            total_recibido += len(data)

    print(f"Archivo recibido correctamente: {output_filename}")
    print(f"Total recibido: {total_recibido} bytes")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
