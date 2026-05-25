import grpc
from concurrent import futures
import file_service_pb2
import file_service_pb2_grpc

PORT = 50051


class FileServiceServicer(file_service_pb2_grpc.FileServiceServicer):

    def Upload(self, request_iterator, context):
        fos = None
        file_name = None
        file_size = 0
        received_bytes = 0

        try:
            for chunk in request_iterator:

                if fos is None:
                    file_name = chunk.file_name

                    if not file_name:
                        file_name = "archivo_recibido.dat"

                    file_size = chunk.file_size

                    fos = open(file_name, "wb")

                    print(f"Iniciando recepción de archivo: {file_name}")
                    print(f"Tamaño declarado: {file_size} bytes")

                data = chunk.data

                if data:
                    fos.write(data)
                    received_bytes += len(data)

                    if file_size > 0:
                        porcentaje = int((received_bytes * 100) / file_size)
                        print(f"\rProgreso de recepción: {porcentaje}%", end="")
                    else:
                        print(f"\rRecibidos: {received_bytes} bytes", end="")

            if fos:
                fos.close()

            print(f"\nRecepción completada de: {file_name}")

            return file_service_pb2.UploadStatus(
                ok=True,
                message=f"Archivo {file_name} recibido correctamente."
            )

        except Exception as e:
            if fos:
                fos.close()

            return file_service_pb2.UploadStatus(
                ok=False,
                message=str(e)
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    file_service_pb2_grpc.add_FileServiceServicer_to_server(
        FileServiceServicer(),
        server
    )

    server.add_insecure_port(f"[::]:{PORT}")

    server.start()

    print(f"Servidor gRPC listo en puerto {PORT}...")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
