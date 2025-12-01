# file_server_gui_grpc.py
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import grpc
from concurrent import futures

import file_transfer_pb2
import file_transfer_pb2_grpc


class FileTransferServicer(file_transfer_pb2_grpc.FileTransferServicer):
    """
    Implementación del servicio gRPC.
    Recibe un stream de FileChunk y escribe el archivo en disco,
    actualizando la GUI con porcentaje y logs.
    """
    def __init__(self, gui_ref):
        self.gui = gui_ref

    def Upload(self, request_iterator, context):
        file_name = None
        total_size = 0
        received = 0
        out_file = None

        try:
            for chunk in request_iterator:
                # Primer chunk: inicializamos archivo y tamaño
                if file_name is None:
                    file_name = chunk.file_name or "archivo_recibido"
                    total_size = chunk.total_size or 0

                    out_path = os.path.join(os.getcwd(), file_name)
                    out_file = open(out_path, "wb")

                    self.gui.log("Conexión entrante...")
                    self.gui.log(
                        f"Iniciando recepción de: {file_name} "
                        f"(tamaño: {total_size} bytes)"
                    )

                # Escribir datos
                if chunk.content:
                    out_file.write(chunk.content)
                    received += len(chunk.content)

                    # Actualizar porcentaje
                    if total_size > 0:
                        progress = int(received * 100 / total_size)
                    else:
                        progress = 0
                    self.gui.update_progress(progress)

            if out_file:
                out_file.close()

            msg = f"Archivo {file_name} recibido correctamente ({received} bytes)."
            self.gui.log(msg)
            self.gui.update_progress(100)

            return file_transfer_pb2.UploadStatus(
                success=True,
                message=msg
            )

        except Exception as e:
            if out_file:
                out_file.close()
            error_msg = f"Error al recibir archivo: {e}"
            self.gui.log(error_msg)
            return file_transfer_pb2.UploadStatus(
                success=False,
                message=error_msg
            )


class FileServerGUIPorcentaje(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Servidor de Archivos gRPC - Porcentaje")
        self.geometry("650x420")

        # --- Componentes GUI (similar a tu Java) ---

        # Panel del puerto
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)

        lbl_port = tk.Label(top_frame, text="Puerto:")
        lbl_port.pack(side=tk.LEFT, padx=5)

        self.txtPort = tk.Entry(top_frame, width=10)
        self.txtPort.insert(0, "50051")
        self.txtPort.pack(side=tk.LEFT, padx=5)

        self.btnStart = tk.Button(top_frame, text="Iniciar servidor",
                                  command=self.start_server)
        self.btnStart.pack(side=tk.LEFT, padx=10)

        # Barra de progreso
        self.progressBar = ttk.Progressbar(self, orient="horizontal",
                                           mode="determinate", length=500)
        self.progressBar.pack(pady=10)

        # Área de log
        lbl_log = tk.Label(self, text="Log del servidor:")
        lbl_log.pack(anchor="w", padx=10)

        self.txtLog = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15)
        self.txtLog.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # --- Servidor gRPC ---
        self.grpc_server = None
        self.server_thread = None
        self.running = False

    # ====== Lógica del servidor ======

    def start_server(self):
        if self.running:
            self.log("El servidor ya está en ejecución.")
            return

        try:
            port = int(self.txtPort.getText() if hasattr(self.txtPort, 'getText')
                       else self.txtPort.get().strip())
        except ValueError:
            self.log("Puerto inválido.")
            return

        self.running = True
        self.btnStart.config(state=tk.DISABLED)
        self.log(f"Iniciando servidor gRPC en el puerto {port}...")

        self.server_thread = threading.Thread(
            target=self._run_grpc_server, args=(port,), daemon=True
        )
        self.server_thread.start()

    def _run_grpc_server(self, port):
        self.grpc_server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10)
        )
        file_transfer_pb2_grpc.add_FileTransferServicer_to_server(
            FileTransferServicer(self), self.grpc_server
        )
        self.grpc_server.add_insecure_port(f"[::]:{port}")
        self.grpc_server.start()
        self.log(f"Servidor gRPC escuchando en el puerto {port}.")
        self.grpc_server.wait_for_termination()

    # ====== Utilidades GUI ======

    def update_progress(self, value):
        def _do():
            self.progressBar["value"] = value
        self.after(0, _do)

    def log(self, msg):
        def _do():
            self.txtLog.insert(tk.END, msg + "\n")
            self.txtLog.see(tk.END)
        self.after(0, _do)


if __name__ == "__main__":
    app = FileServerGUIPorcentaje()
    app.mainloop()
