import socket
import os
import sys

def crear_archivo_prueba(ruta="example.bin", tam_mb=50):
    if os.path.exists(ruta):
        print(f"Archivo existente: {ruta}")
        return

    print(f"Generando archivo de prueba de {tam_mb} MB...")
    with open(ruta, "wb") as f:
        f.write(os.urandom(tam_mb * 1024 * 1024))

    print(f"Archivo generado: {ruta}")


def main():
    SERVER = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    PORT = 12345
    FILE_PATH = "example.bin"

    crear_archivo_prueba(FILE_PATH, 50)

    if not os.path.exists(FILE_PATH):
        print("El archivo no existe:", FILE_PATH)
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER, PORT))
        print(f"Conectado al servidor {SERVER}:{PORT}")

        filename = os.path.basename(FILE_PATH).encode()
        client_socket.sendall(len(filename).to_bytes(4, "big"))
        client_socket.sendall(filename)

        total_size = os.path.getsize(FILE_PATH)
        sent = 0

        with open(FILE_PATH, "rb") as f:
            while True:
                chunk = f.read(4096)

                if not chunk:
                    break

                client_socket.sendall(len(chunk).to_bytes(4, "big"))
                client_socket.sendall(chunk)

                sent += len(chunk)
                progress = (sent / total_size) * 100
                print(f"Progreso envío: {progress:.2f}%")

        client_socket.sendall((0).to_bytes(4, "big"))

        print("Archivo enviado exitosamente.")

    except ConnectionRefusedError:
        print("Error: conexión rechazada. Verifica que el servidor esté encendido.")
    except TimeoutError:
        print("Error: tiempo de conexión agotado.")
    except BrokenPipeError:
        print("Error: el servidor cerró la conexión.")
    except ConnectionResetError:
        print("Error: la conexión fue reiniciada por el servidor.")
    except Exception as e:
        print("Error inesperado:", e)

    finally:
        try:
            client_socket.close()
        except:
            pass


if __name__ == "__main__":
    main()
