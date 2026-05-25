import socket
import os

HOST = "0.0.0.0"
PORT = 12345

def recibir_exactamente(sock, n):
    datos = b""

    while len(datos) < n:
        parte = sock.recv(n - len(datos))

        if not parte:
            return None

        datos += parte

    return datos


def main():
    os.makedirs("recibidos", exist_ok=True)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))

    server_socket.listen(5)

    print(f"Servidor escuchando en {HOST}:{PORT}")
    print("Esperando conexiones...")

    while True:
        client_socket, addr = server_socket.accept()

        print(f"\nCliente conectado desde: {addr}")

        try:
            filename_length_bytes = recibir_exactamente(client_socket, 4)

            if not filename_length_bytes:
                print("No se recibió el tamaño del nombre.")
                client_socket.close()
                continue

            filename_length = int.from_bytes(filename_length_bytes, "big")

            filename_bytes = recibir_exactamente(client_socket, filename_length)

            if not filename_bytes:
                print("No se recibió el nombre del archivo.")
                client_socket.close()
                continue

            filename = filename_bytes.decode()

            ip_cliente = addr[0].replace(".", "_")
            puerto_cliente = addr[1]

            output_filename = os.path.join(
                "recibidos",
                f"received_{ip_cliente}_{puerto_cliente}_{os.path.basename(filename)}"
            )

            print(f"Nombre del archivo recibido: {filename}")
            print(f"Guardando como: {output_filename}")

            total_recibido = 0

            with open(output_filename, "wb") as f:
                while True:
                    chunk_size_bytes = recibir_exactamente(client_socket, 4)

                    if not chunk_size_bytes:
                        print("Conexión cerrada inesperadamente.")
                        break

                    chunk_size = int.from_bytes(chunk_size_bytes, "big")

                    if chunk_size == 0:
                        break

                    data = recibir_exactamente(client_socket, chunk_size)

                    if not data:
                        print("Chunk incompleto.")
                        break

                    f.write(data)
                    total_recibido += len(data)

                    print(
                        f"Recibidos: {total_recibido / (1024 * 1024):.2f} MB",
                        end="\r"
                    )

            print(f"\nArchivo guardado en: {output_filename}")
            print(f"Total recibido: {total_recibido / (1024 * 1024):.2f} MB")

        except Exception as e:
            print("Error:", e)

        finally:
            client_socket.close()
            print("Conexión cerrada.")


if __name__ == "__main__":
    main()
