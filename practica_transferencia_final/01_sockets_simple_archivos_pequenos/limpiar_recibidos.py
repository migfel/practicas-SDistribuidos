import os
import shutil

CARPETA = "recibidos"

if os.path.exists(CARPETA):
    shutil.rmtree(CARPETA)
    print("Carpeta eliminada.")

os.makedirs(CARPETA, exist_ok=True)

print("Carpeta limpia y recreada.")
