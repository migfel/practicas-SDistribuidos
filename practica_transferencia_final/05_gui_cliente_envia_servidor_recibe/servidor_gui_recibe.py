import socket
import struct
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk


class FileServerGUIPorcentaje:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor de Recepción de Archivos")
        self.root.geometry("600x350")

        self.server_socket = None
        self.running = False

        self.build_gui()

    def build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Puerto:").grid(row=0, column=0, sticky="w", padx=4, pady=4)

        self.txt_port = tk.Entry(frame)
        self.txt_port.insert(0, "12345")
        self.txt_port.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        self.btn_start = tk.Button(frame, text="Iniciar servidor", command=self.on_start_server)
        self.btn_start.grid(row=0, column=2, padx=4, pady=4)

        frame.columnconfigure(1, weight=1)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=10)

        self.progress_label = tk.Label(self.root, text="0%")
        self.progress_label.pack()

        self.txt_log = scrolledtext.ScrolledText(self.root, height=10, state="disabled")
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=10)

    def on_start_server(self):
        if self.running:
            messagebox.showinfo("Info", "El servidor ya está en ejecución.")
            return

        try:
            port = int(self.txt_port.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido.")
            return

        self.running = True
        self.btn_start.config(state="disabled")
        self.log(f"Iniciando servidor en puerto {port}...")

        thread = threading.Thread(target=self.start_server, args=(port,), daemon=True)
        thread.start()

    def start_server(self, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", port))
            self.server_socket.listen()

            self.log(f"Servidor listo en puerto {port}...")

            while self.running:
                client, address = self.server_socket.accept()
                self.log(f"Cliente conectado: {address}")

                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client,),
                    daemon=True
                )
                thread.start()

        except Exception as e:
            self.log(f"Error en el servidor: {e}")

        finally:
            self.running = False
            self.root.after(0, lambda: self.btn_start.config(state="normal"))

    def recibir_exactamente(self, sock, cantidad):
        datos = b""

        while len(datos) < cantidad:
            bloque = sock.recv(cantidad - len(datos))

            if not bloque:
                return None

            datos += bloque

        return datos

    def recibir_utf(self, sock):
        longitud_bytes = self.recibir_exactamente(sock, 2)

        if not longitud_bytes:
            raise ConnectionError("No se pudo leer la longitud del nombre del archivo.")

        longitud = struct.unpack(">H", longitud_bytes)[0]

        datos = self.recibir_exactamente(sock, longitud)

        if not datos:
            raise ConnectionError("No se pudo leer el nombre del archivo.")

        return datos.decode("utf-8")

    def handle_client(self, client):
        try:
            with client:
                # 1. Leer nombre del archivo
                file_name = self.recibir_utf(client)

                # 2. Leer tamaño del archivo
                size_bytes = self.recibir_exactamente(client, 8)

                if not size_bytes:
                    raise ConnectionError("No se pudo leer el tamaño del archivo.")

                file_size = struct.unpack(">Q", size_bytes)[0]

                self.log(f"Recibiendo archivo: {file_name} ({file_size} bytes)")

                output_name = "received_" + file_name
                total_read = 0
                last_percent = -1
                self.update_progress(0)

                with open(output_name, "wb") as output_file:
                    while total_read < file_size:
                        remaining = file_size - total_read
                        data = client.recv(min(8192, remaining))

                        if not data:
                            break

                        output_file.write(data)
                        total_read += len(data)

                        if file_size > 0:
                            percent = int((total_read * 100) / file_size)

                            if percent != last_percent:
                                last_percent = percent
                                self.update_progress(percent)

                self.update_progress(100)
                self.log(f"Recepción completada de: {file_name}")

        except Exception as e:
            self.log(f"Error manejando cliente: {e}")

    def update_progress(self, value):
        self.root.after(0, lambda: self._update_progress_gui(value))

    def _update_progress_gui(self, value):
        self.progress["value"] = value
        self.progress_label.config(text=f"{value}%")

    def log(self, message):
        self.root.after(0, lambda: self._log_gui(message))

    def _log_gui(self, message):
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileServerGUIPorcentaje(root)
    root.mainloop()
