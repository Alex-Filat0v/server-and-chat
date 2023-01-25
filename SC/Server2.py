import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost", 1234))
server.listen(10)
print("server is working")

while True:
	user_socket, adress = server.accept()
	user_socket.send("Fuck you".encode("utf-8"))
	print(f"user {adress} connected!")
	while True:
		data = user_socket.recv(2048)
		print(data.decode("utf-8"))
