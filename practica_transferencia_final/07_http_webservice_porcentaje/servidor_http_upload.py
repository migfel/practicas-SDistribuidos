from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = 8000
BUFFER_SIZE = 64 * 1024


class FileUploadHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/upload":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada.")
            return

        file_name = self.headers.get("X-File-Name")
        file_size_header = self.headers.get("X-File-Size")

        if not file_name:
            file_name = "archivo_recibido.bin"

        try:
            file_size = int(file_size_header) if file_size_header else -1
        except ValueError:
            file_size = -1

        print("Recibiendo archivo:", file_name)

        if file_size > 0:
            print("Tamaño reportado:", file_size, "bytes")

        output_file = "recibido_" + os.path.basename(file_name)

        total_read = 0
        last_percent = -1

        try:
            with open(output_file, "wb") as f:
                while True:
                    chunk = self.rfile.read(min(BUFFER_SIZE, file_size - total_read) if file_size > 0 else BUFFER_SIZE)

                    if not chunk:
                        break

                    f.write(chunk)
                    total_read += len(chunk)

                    if file_size > 0:
                        percent = (total_read * 100) // file_size

                        if percent != last_percent:
                            print(f"\rProgreso servidor: {percent}%", end="")
                            last_percent = percent

                    if file_size > 0 and total_read >= file_size:
                        break

            print("\nRecepción completada de:", os.path.abspath(output_file))

            response = "Archivo recibido correctamente en el servidor."
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(response.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

        except Exception as e:
            error = f"Error al recibir archivo: {e}"
            print(error)

            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(error.encode("utf-8"))

    def do_GET(self):
        response = "Servidor activo. Usa POST en /upload para enviar archivos."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


def main():
    server = HTTPServer(("0.0.0.0", PORT), FileUploadHandler)
    print(f"Servidor HTTP listo en puerto {PORT}...")
    print(f"Endpoint: http://localhost:{PORT}/upload")
    server.serve_forever()


if __name__ == "__main__":
    main()
