import subprocess
import time
import sys

if len(sys.argv) < 2:
    print("Uso: python3 stress_100_etapa3.py <IP_SERVIDOR>")
    sys.exit(1)

IP_SERVIDOR = sys.argv[1]
NUM_CLIENTES = 100

for i in range(NUM_CLIENTES):
    subprocess.Popen(
        ["python3", "cliente_porcentaje.py", IP_SERVIDOR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Cliente {i+1} enviado al servidor {IP_SERVIDOR}")
    time.sleep(0.02)

print("Se lanzaron 100 clientes hacia Etapa 3.")
