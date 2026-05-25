import os
import shutil

CARPETA = "recibidos"

if os.path.exists(CARPETA):

    archivos = os.listdir(CARPETA)

    total = len(archivos)

    for archivo in archivos:
        ruta = os.path.join(CARPETA, archivo)

        try:
            if os.path.isfile(ruta):
                os.remove(ruta)
        except Exception as e:
            print(f"Error eliminando {archivo}: {e}")

    print(f"Se eliminaron {total} archivos.")

else:
    print("La carpeta 'recibidos' no existe.")