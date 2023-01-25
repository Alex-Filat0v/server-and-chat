import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 1234))

while True:
	data = client.recv(2048)
	print(data.decode("utf-8"))
	while True:
		client.send(input(":").encode("utf-8"))
