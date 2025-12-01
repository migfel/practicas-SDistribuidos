# file_client_gui_grpc.py
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext

import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc


class FileClientGUIPorcentaje(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cliente de Archivos gRPC - Porcentaje")
        self.geometry("650x420")

        self.selected_file = None

        # --- GUI similar a tu Java ---

        # Línea Host
        host_frame = tk.Frame(self)
        host_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(host_frame, text="Host:").pack(side=tk.LEFT)
        self.txtHost = tk.Entry(host_frame, width=20)
        self.txtHost.insert(0, "localhost")
        self.txtHost.pack(side=tk.LEFT, padx=5)

        # Línea Puerto
        port_frame = tk.Frame(self)
        port_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(port_frame, text="Puerto:").pack(side=tk.LEFT)
        self.txtPort = tk.Entry(port_frame, width=10)
        self.txtPort.insert(0, "50051")
        self.txtPort.pack(side=tk.LEFT, padx=5)

        # Línea Archivo
        file_frame = tk.Frame(self)
        file_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(file_frame, text="Archivo:").pack(side=tk.LEFT)
        self.txtFile = tk.Entry(file_frame, width=40)
        self.txtFile.pack(side=tk.LEFT, padx=5)

        self.btnBrowse = tk.Button(file_frame, text="Buscar",
                                   command=self.browse_file)
        self.btnBrowse.pack(side=tk.LEFT, padx=5)

        # Botón Enviar
        self.btnSend = tk.Button(self, text="Enviar archivo",
                                 command=self.send_button_clicked)
        self.btnSend.pack(pady=5)

        # Barra de progreso
        self.progressBar = ttk.Progressbar(self, orient="horizontal",
                                           mode="determinate", length=500)
        self.progressBar.pack(pady=10)

        # Área de log
        lbl_log = tk.Label(self, text="Log del cliente:")
        lbl_log.pack(anchor="w", padx=10)

        self.txtLog = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15)
        self.txtLog.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # ====== Acciones GUI ======

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.selected_file = path
            self.txtFile.delete(0, tk.END)
            self.txtFile.insert(0, path)
            self.log(f"Archivo seleccionado: {path}")

    def send_button_clicked(self):
        host = self.txtHost.get().strip()
        port_str = self.txtPort.get().strip()
        file_path = self.txtFile.get().strip()

        if not host or not port_str:
            self.log("Host o puerto vacíos.")
            return

        if not file_path:
            self.log("Seleccione un archivo.")
            return

        if not os.path.isfile(file_path):
            self.log(f"El archivo no existe: {file_path}")
            return

        try:
            port = int(port_str)
        except ValueError:
            self.log("Puerto inválido.")
            return

        self.btnSend.config(state=tk.DISABLED)
        self.progressBar["value"] = 0

        # Lanzar envío en hilo para no bloquear la GUI
        thread = threading.Thread(
            target=self.send_file, args=(host, port, file_path), daemon=True
        )
        thread.start()

    # ====== Lógica de envío con gRPC ======

    def send_file(self, host, port, file_path):
        file_name = os.path.basename(file_path)
        total_size = os.path.getsize(file_path)

        self.log(f"Conectando a {host}:{port}...")
        try:
            with grpc.insecure_channel(f"{host}:{port}") as channel:
                stub = file_transfer_pb2_grpc.FileTransferStub(channel)

                def request_generator():
                    chunk_size = 64 * 1024  # 64 KB (similar idea a tu Java)
                    sent = 0
                    with open(file_path, "rb") as f:
                        while True:
                            data = f.read(chunk_size)
                            if not data:
                                break
                            sent += len(data)

                            # Actualizar porcentaje
                            if total_size > 0:
                                progress = int(sent * 100 / total_size)
                            else:
                                progress = 0
                            self.update_progress(progress)

                            yield file_transfer_pb2.FileChunk(
                                file_name=file_name,
                                total_size=total_size,
                                content=data
                            )

                self.log(
                    f"Enviando archivo: {file_name} "
                    f"(tamaño: {total_size} bytes)..."
                )

                response = stub.Upload(request_generator())

                if response.success:
                    self.log(f"Servidor respondió OK: {response.message}")
                    self.update_progress(100)
                else:
                    self.log(f"Servidor reportó error: {response.message}")

        except Exception as e:
            self.log(f"Error al enviar archivo: {e}")
        finally:
            self.btnSend.config(state=tk.NORMAL)

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
    app = FileClientGUIPorcentaje()
    app.mainloop()
