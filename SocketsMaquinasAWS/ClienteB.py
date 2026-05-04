import socket

client = socket.socket()
client.connect(("10.0.10.125", 5000))

client.send(b"Hola servidor")
respuesta = client.recv(1024)

print("Respuesta:", respuesta.decode())
client.close()