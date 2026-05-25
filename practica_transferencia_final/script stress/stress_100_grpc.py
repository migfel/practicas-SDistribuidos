import subprocess
import time
import sys

if len(sys.argv) < 2:
    print("Uso: python3 stress_100_grpc.py <IP_SERVIDOR>")
    sys.exit(1)

IP_SERVIDOR = sys.argv[1]
NUM_CLIENTES = 100

for i in range(NUM_CLIENTES):
    subprocess.Popen(
        ["python3", "FileClientPorcentajeGrpc.py", IP_SERVIDOR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Cliente gRPC {i+1} enviado a {IP_SERVIDOR}")
    time.sleep(0.02)

print("Se lanzaron 100 clientes gRPC.")
