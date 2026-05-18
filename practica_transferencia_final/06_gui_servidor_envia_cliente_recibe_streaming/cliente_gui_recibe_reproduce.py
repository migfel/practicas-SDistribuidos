import socket
import threading
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BUFFER_SIZE = 8192  # 8 KB
BUFFER_TO_START_MB = 5  # Umbral de buffer para iniciar reproducción (MB)


class FileClientGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cliente - Recepción y Reproducción de Video")
        self.geometry("650x380")

        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Host
        ttk.Label(top_frame, text="Host:").grid(row=0, column=0, sticky="w")
        self.entry_host = ttk.Entry(top_frame)
        self.entry_host.insert(0, "localhost")
        self.entry_host.grid(row=0, column=1, sticky="we", padx=5)

        # Puerto
        ttk.Label(top_frame, text="Puerto:").grid(row=1, column=0, sticky="w")
        self.entry_port = ttk.Entry(top_frame)
        self.entry_port.insert(0, "12345")
        self.entry_port.grid(row=1, column=1, sticky="we", padx=5)

        # Directorio salida
        ttk.Label(top_frame, text="Directorio salida:").grid(row=2, column=0, sticky="w")
        self.entry_dir = ttk.Entry(top_frame)
        self.entry_dir.grid(row=2, column=1, sticky="we", padx=5)

        btn_browse_dir = ttk.Button(top_frame, text="Elegir...", command=self.on_select_dir)
        btn_browse_dir.grid(row=2, column=2, padx=5)

        # Botón conectar
        self.btn_connect = ttk.Button(top_frame, text="Conectar y recibir video",
                                      command=self.on_connect)
        self.btn_connect.grid(row=3, column=1, columnspan=2, pady=5, sticky="e")

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

    def on_select_dir(self):
        directory = filedialog.askdirectory(title="Selecciona directorio de salida")
        if directory:
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, directory)
            self.log(f"Directorio de salida seleccionado: {directory}")

    def on_connect(self):
        host = self.entry_host.get().strip()
        try:
            port = int(self.entry_port.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido.")
            return

        # Directorio salida
        out_dir = self.entry_dir.get().strip()
        if not out_dir:
            out_dir = "."  # carpeta actual

        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el directorio: {e}")
                return

        # Deshabilitar botón durante la recepción
        self.btn_connect.config(state="disabled")
        self.log(f"Conectando a {host}:{port} ...")

        thread = threading.Thread(target=self.receive_file, args=(host, port, out_dir), daemon=True)
        thread.start()

    def recv_line(self, sock):
        """
        Lee una línea terminada en '\n' desde el socket.
        """
        data = b""
        while True:
            ch = sock.recv(1)
            if not ch:
                break
            if ch == b"\n":
                break
            data += ch
        return data.decode("utf-8")

    def receive_file(self, host, port, output_dir):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                self.log(f"Conectado a servidor {host}:{port}")

                # 1. Leer nombre del archivo (línea)
                file_name = self.recv_line(s).strip()

                # 2. Leer tamaño
                size_str = self.recv_line(s).strip()
                file_size = int(size_str)

                self.log(f"Recibiendo archivo: {file_name} ({file_size} bytes)")

                # Nombre de salida
                out_path = os.path.join(output_dir, "received_" + file_name)
                self.log(f"Guardando como: {out_path}")

                total_read = 0
                last_percent = 0
                self.set_progress(0)

                buffer_to_start = min(file_size, BUFFER_TO_START_MB * 1024 * 1024)
                playback_started = False

                with open(out_path, "wb") as f:
                    while total_read < file_size:
                        chunk = s.recv(BUFFER_SIZE)
                        if not chunk:
                            break

                        f.write(chunk)
                        total_read += len(chunk)

                        if file_size > 0:
                            percent = int(total_read * 100 / file_size)
                            if percent != last_percent:
                                last_percent = percent
                                self.set_progress(percent)
                                self.log(f"Progreso: {percent}%")

                        # Iniciar reproducción cuando haya suficiente buffer
                        if (not playback_started) and total_read >= buffer_to_start:
                            playback_started = True
                            self.log("Buffer suficiente, iniciando reproducción del video...")
                            self.start_playback(out_path)

                self.set_progress(100)
                self.log("Recepción completada.")

                # Si el archivo era pequeño y nunca se inició reproducción
                if not playback_started:
                    self.log("Archivo pequeño, iniciando reproducción al final.")
                    self.start_playback(out_path)

        except Exception as e:
            self.log(f"Error recibiendo archivo: {e}")
        finally:
            # Rehabilitar botón
            self.after(0, lambda: self.btn_connect.config(state="normal"))

    def start_playback(self, filepath):
        """
        Abre el archivo de video con el reproductor por defecto del SO.
        Se lanza en un hilo aparte para no bloquear la GUI.
        """
        def _open():
            try:
                if sys.platform.startswith("win"):
                    os.startfile(filepath)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", filepath])
                else:
                    subprocess.Popen(["xdg-open", filepath])
            except Exception as e:
                self.log(f"No se pudo abrir el video automáticamente: {e}")

        threading.Thread(target=_open, daemon=True).start()


if __name__ == "__main__":
    app = FileClientGUI()
    app.mainloop()
