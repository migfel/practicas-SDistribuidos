import grpc
import file_service_pb2
import file_service_pb2_grpc
import os

HOST = "localhost:12345"
FILE_PATH = "uno.mp4"


def generar_chunks(file_path):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    sent_bytes = 0

    with open(file_path, "rb") as f:
        buffer_size = 64 * 1024

        data = f.read(buffer_size)

        if not data:
            return

        sent_bytes += len(data)

        porcentaje = int((sent_bytes * 100) / file_size)
        print(f"\rProgreso de envío: {porcentaje}%", end="")

        yield file_service_pb2.FileChunk(
            file_name=file_name,
            file_size=file_size,
            data=data
        )

        while True:
            data = f.read(buffer_size)

            if not data:
                break

            sent_bytes += len(data)

            porcentaje = int((sent_bytes * 100) / file_size)
            print(f"\rProgreso de envío: {porcentaje}%", end="")

            yield file_service_pb2.FileChunk(
                data=data
            )


def main():
    if not os.path.exists(FILE_PATH):
        print("El archivo no existe.")
        return

    file_size = os.path.getsize(FILE_PATH)

    print(f"Iniciando envío de: {FILE_PATH}")
    print(f"Tamaño: {file_size} bytes")

    channel = grpc.insecure_channel(HOST)

    stub = file_service_pb2_grpc.FileServiceStub(channel)

    response = stub.Upload(generar_chunks(FILE_PATH))

    print("\nRespuesta del servidor:", response.message)
    print("Envío completado (gRPC).")


if __name__ == "__main__":
    main()
