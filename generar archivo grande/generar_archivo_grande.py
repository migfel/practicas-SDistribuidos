import os

nombre_archivo = "archivo_grande_prueba.bin"
tamano_mb = 500

with open(nombre_archivo, "wb") as archivo:
    archivo.write(os.urandom(tamano_mb * 1024 * 1024))

print(f"Archivo generado: {nombre_archivo}")
print(f"Tamaño: {tamano_mb} MB")