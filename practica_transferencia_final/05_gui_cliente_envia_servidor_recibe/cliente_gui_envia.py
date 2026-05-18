import socket
import struct
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk


class FileClientGUIPorcentaje:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente de Envío de Archivos")
        self.root.geometry("600x350")

        self.selected_file = None

        self.build_gui()

    def build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Host:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.txt_host = tk.Entry(frame)
        self.txt_host.insert(0, "localhost")
        self.txt_host.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        tk.Label(frame, text="Puerto:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.txt_port = tk.Entry(frame)
        self.txt_port.insert(0, "12345")
        self.txt_port.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

        tk.Label(frame, text="Archivo:").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.txt_file = tk.Entry(frame, state="readonly")
        self.txt_file.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

        btn_browse = tk.Button(frame, text="Seleccionar...", command=self.on_browse_file)
        btn_browse.grid(row=2, column=2, padx=4, pady=4)

        btn_send = tk.Button(frame, text="Enviar archivo", command=self.on_send_file)
        btn_send.grid(row=3, column=1, columnspan=2, sticky="ew", padx=4, pady=4)

        frame.columnconfigure(1, weight=1)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=10)

        self.progress_label = tk.Label(self.root, text="0%")
        self.progress_label.pack()

        self.txt_log = scrolledtext.ScrolledText(self.root, height=8, state="disabled")
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=10)

    def on_browse_file(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.selected_file = file_path

            self.txt_file.config(state="normal")
            self.txt_file.delete(0, tk.END)
            self.txt_file.insert(0, file_path)
            self.txt_file.config(state="readonly")

            size = os.path.getsize(file_path)
            self.log(f"Archivo seleccionado: {os.path.basename(file_path)} ({size} bytes)")

    def on_send_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Primero selecciona un archivo.")
            return

        host = self.txt_host.get().strip()

        try:
            port = int(self.txt_port.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido.")
            return

        thread = threading.Thread(
            target=self.send_file,
            args=(host, port, self.selected_file),
            daemon=True
        )
        thread.start()

    def enviar_utf(self, sock, texto):
        datos = texto.encode("utf-8")
        sock.sendall(struct.pack(">H", len(datos)))
        sock.sendall(datos)

    def send_file(self, host, port, file_path):
        if not os.path.exists(file_path):
            self.log(f"El archivo no existe: {file_path}")
            return

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))

                self.log(f"Conectado a {host}:{port}")
                self.log(f"Enviando archivo: {file_name} ({file_size} bytes)")

                # 1. Enviar nombre del archivo
                self.enviar_utf(sock, file_name)

                # 2. Enviar tamaño del archivo como long de Java: 8 bytes
                sock.sendall(struct.pack(">Q", file_size))

                # 3. Enviar contenido
                total_sent = 0
                last_percent = -1
                self.update_progress(0)

                with open(file_path, "rb") as f:
                    while True:
                        data = f.read(8192)

                        if not data:
                            break

                        sock.sendall(data)
                        total_sent += len(data)

                        if file_size > 0:
                            percent = int((total_sent * 100) / file_size)

                            if percent != last_percent:
                                last_percent = percent
                                self.update_progress(percent)

                self.update_progress(100)
                self.log("Envío completado.")

        except Exception as e:
            self.log(f"Error en el cliente: {e}")

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
    app = FileClientGUIPorcentaje(root)
    root.mainloop()
