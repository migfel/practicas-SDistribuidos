import os
import requests
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
URL = f"http://{HOST}:8000/upload"

FILE_PATH = "uno.mp4"
BUFFER_SIZE = 64 * 1024


def generar_archivo_prueba(ruta, tam_mb=50):
    if os.path.exists(ruta):
        print(f"Archivo existente: {ruta}")
        return

    print(f"Generando archivo de prueba de {tam_mb} MB...")
    with open(ruta, "wb") as f:
        f.write(os.urandom(tam_mb * 1024 * 1024))

    print(f"Archivo generado: {ruta}")


def main():
    try:
        generar_archivo_prueba(FILE_PATH, 50)

        file_size = os.path.getsize(FILE_PATH)
        file_name = os.path.basename(FILE_PATH)

        headers = {
            "X-File-Name": file_name,
            "X-File-Size": str(file_size),
            "Content-Type": "application/octet-stream"
        }

        print("Conectado al servidor HTTP. Enviando archivo:", file_name)
        print("Tamaño del archivo:", file_size, "bytes")

        total_sent = 0
        last_percent = -1

        def file_generator():
            nonlocal total_sent, last_percent

            with open(FILE_PATH, "rb") as f:
                while True:
                    chunk = f.read(BUFFER_SIZE)

                    if not chunk:
                        break

                    total_sent += len(chunk)

                    percent = (total_sent * 100) // file_size

                    if percent != last_percent:
                        print(f"\rProgreso cliente: {percent}%", end="")
                        last_percent = percent

                    yield chunk

        response = requests.post(
            URL,
            data=file_generator(),
            headers=headers
        )

        print("\nEnvío completado. Esperando respuesta del servidor...")
        print("Código de respuesta:", response.status_code)
        print("Respuesta del servidor:")
        print(response.text)

    except Exception as e:
        print("Error:")
        print(e)


if __name__ == "__main__":
    main()
