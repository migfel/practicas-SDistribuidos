import grpc
import file_service_pb2
import file_service_pb2_grpc
import os
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = 50051
FILE_PATH = "uno.mp4"


def generar_archivo_prueba(ruta, tam_mb=50):
    if os.path.exists(ruta):
        print(f"Archivo existente: {ruta}")
        return

    print(f"Generando archivo de prueba de {tam_mb} MB...")
    with open(ruta, "wb") as f:
        f.write(os.urandom(tam_mb * 1024 * 1024))

    print(f"Archivo generado: {ruta}")


def generar_chunks(file_path):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    sent_bytes = 0
    buffer_size = 64 * 1024

    with open(file_path, "rb") as f:
        primer_chunk = True

        while True:
            data = f.read(buffer_size)

            if not data:
                break

            sent_bytes += len(data)

            porcentaje = int((sent_bytes * 100) / file_size)
            print(f"\rProgreso de envío: {porcentaje}%", end="")

            if primer_chunk:
                primer_chunk = False

                yield file_service_pb2.FileChunk(
                    file_name=file_name,
                    file_size=file_size,
                    data=data
                )
            else:
                yield file_service_pb2.FileChunk(
                    data=data
                )


def main():
    generar_archivo_prueba(FILE_PATH, 50)

    file_size = os.path.getsize(FILE_PATH)

    print(f"Iniciando envío de: {FILE_PATH}")
    print(f"Tamaño: {file_size} bytes")

    server = f"{HOST}:{PORT}"

    channel = grpc.insecure_channel(server)

    stub = file_service_pb2_grpc.FileServiceStub(channel)

    response = stub.Upload(generar_chunks(FILE_PATH))

    print("\nRespuesta del servidor:", response.message)
    print("Envío completado (gRPC).")


if __name__ == "__main__":
    main()
