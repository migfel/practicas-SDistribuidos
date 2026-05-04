import socket

server = socket.socket()
server.bind(("0.0.0.0", 5000))
server.listen(1)

print("Esperando conexión...")

conn, addr = server.accept()
print("Conectado desde:", addr)

data = conn.recv(1024)
print("Mensaje recibido:", data.decode())

conn.send(b"Hola desde servidor")
conn.close()