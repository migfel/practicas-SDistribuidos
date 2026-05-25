import socket
import os

HOST = "0.0.0.0"
PORT = 12345
GUARDAR_ARCHIVO = False

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
    server_socket.listen(1)

    print(f"Servidor simple escuchando en {HOST}:{PORT}")
    print("Atiende un cliente a la vez. Esperando conexiones...")

    contador = 0

    while True:
        client_socket, addr = server_socket.accept()
        contador += 1

        print(f"\nCliente #{contador} conectado desde: {addr}")

        try:
            filename_length_bytes = recibir_exactamente(client_socket, 4)
            if not filename_length_bytes:
                continue

            filename_length = int.from_bytes(filename_length_bytes, "big")
            filename_bytes = recibir_exactamente(client_socket, filename_length)
            if not filename_bytes:
                continue

            filename = filename_bytes.decode()
            print(f"Recibiendo: {filename}")

            ip_cliente = addr[0].replace(".", "_")
            puerto_cliente = addr[1]

            output_filename = os.path.join(
                "recibidos",
                f"received_{contador}_{ip_cliente}_{puerto_cliente}_{os.path.basename(filename)}"
            )

            total_recibido = 0

            if GUARDAR_ARCHIVO:
                f = open(output_filename, "wb")
            else:
                f = None

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

                if GUARDAR_ARCHIVO:
                    f.write(data)

                total_recibido += len(data)

            if f:
                f.close()

            print(f"Cliente #{contador} terminado.")
            print(f"Total recibido: {total_recibido / (1024 * 1024):.2f} MB")

            if GUARDAR_ARCHIVO:
                print(f"Archivo guardado en: {output_filename}")
            else:
                print("Modo stress: archivo recibido pero no guardado.")

        except Exception as e:
            print("Error:", e)

        finally:
            client_socket.close()
            print("Conexión cerrada. Esperando siguiente cliente...")

if __name__ == "__main__":
    main()
