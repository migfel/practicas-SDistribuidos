import socket
import threading
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BUFFER_SIZE = 8192  # 8 KB


class FileServerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Servidor - Envío de Video")
        self.geometry("650x350")

        self.server_socket = None
        self.running = False
        self.selected_file = None

        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Puerto
        ttk.Label(top_frame, text="Puerto:").grid(row=0, column=0, sticky="w")
        self.entry_port = ttk.Entry(top_frame)
        self.entry_port.insert(0, "12345")
        self.entry_port.grid(row=0, column=1, sticky="we", padx=5)

        # Archivo
        ttk.Label(top_frame, text="Archivo de video:").grid(row=1, column=0, sticky="w")
        self.entry_file = ttk.Entry(top_frame, state="readonly")
        self.entry_file.grid(row=1, column=1, sticky="we", padx=5)

        btn_browse = ttk.Button(top_frame, text="Seleccionar...", command=self.on_browse_file)
        btn_browse.grid(row=1, column=2, padx=5)

        self.btn_start = ttk.Button(top_frame, text="Esperar cliente y enviar",
                                    command=self.on_start_server)
        self.btn_start.grid(row=2, column=1, columnspan=2, pady=5, sticky="e")

        top_frame.columnconfigure(1, weight=1)

        # Barra de progreso
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate", maximum=100)
        self.progress.pack(fill=tk.X, padx=10, pady=5)

        # Log
        self.text_log = tk.Text(self, height=10, state="disabled")
        self.text_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def log(self, message):
        def append():
            self.text_log.configure(state="normal")
            self.text_log.insert(tk.END, message + "\n")
            self.text_log.see(tk.END)
            self.text_log.configure(state="disabled")
        self.after(0, append)

    def set_progress(self, value):
        def upd():
            self.progress["value"] = value
        self.after(0, upd)

    def on_browse_file(self):
        file_path = filedialog.askopenfilename(title="Selecciona archivo de video")
        if file_path:
            self.selected_file = file_path
            self.entry_file.configure(state="normal")
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file_path)
            self.entry_file.configure(state="readonly")
            size = os.path.getsize(file_path)
            self.log(f"Archivo seleccionado: {os.path.basename(file_path)} ({size} bytes)")

    def on_start_server(self):
        if self.running:
            messagebox.showinfo("Info", "El servidor ya está en ejecución.")
            return

        if not self.selected_file:
            messagebox.showerror("Error", "Selecciona primero un archivo de video.")
            return

        try:
            port = int(self.entry_port.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido.")
            return

        self.running = True
        self.btn_start.config(state="disabled")
        self.entry_port.config(state="disabled")
        self.log(f"Iniciando servidor en puerto {port}. Esperando a que un cliente se conecte...")

        thread = threading.Thread(target=self.start_server, args=(port, self.selected_file), daemon=True)
        thread.start()

    def start_server(self, port, file_path):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("0.0.0.0", port))
                s.listen(1)
                client_socket, addr = s.accept()
                self.log(f"Cliente conectado desde: {addr}")

                with client_socket:
                    self.send_file_to_client(client_socket, file_path)

            self.log("Servidor finalizó envío y cerró conexión.")
        except Exception as e:
            self.log(f"Error en el servidor: {e}")
        finally:
            self.running = False
            self.after(0, self.reset_controls)

    def reset_controls(self):
        self.btn_start.config(state="normal")
        self.entry_port.config(state="normal")
        self.set_progress(0)

    def send_file_to_client(self, client_socket, file_path):
        if not os.path.exists(file_path):
            self.log(f"El archivo no existe: {file_path}")
            return

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        self.log(f"Enviando archivo: {file_name} ({file_size} bytes)")

        try:
            # 1. Enviar nombre (línea)
            header_name = (file_name + "\n").encode("utf-8")
            client_socket.sendall(header_name)

            # 2. Enviar tamaño (línea)
            header_size = (str(file_size) + "\n").encode("utf-8")
            client_socket.sendall(header_size)

            # 3. Enviar contenido
            total_sent = 0
            last_percent = 0
            self.set_progress(0)

            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    client_socket.sendall(chunk)
                    total_sent += len(chunk)

                    if file_size > 0:
                        percent = int(total_sent * 100 / file_size)
                        if percent != last_percent:
                            last_percent = percent
                            self.set_progress(percent)
            self.set_progress(100)
            self.log("Envío completado.")
        except Exception as e:
            self.log(f"Error enviando archivo: {e}")


if __name__ == "__main__":
    app = FileServerGUI()
    app.mainloop()
