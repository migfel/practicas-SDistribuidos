Instalar dependencias:

pip install grpcio grpcio-tools

Generar archivos desde el proto:

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file_service_python.proto

Ejecutar servidor:

python FileServerPorcentajeGrpc.py

Ejecutar cliente:

python FileClientPorcentajeGrpc.py
