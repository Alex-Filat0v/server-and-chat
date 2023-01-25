import sys
import pickle
import random
import math
import rsa
import socket
import time

host = socket.gethostbyname(socket.gethostname())
port = 9090
clients = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
quit = False

print("Server started")

while not quit:
	try:
		message, address = s.recvfrom(1024)

		if address not in clients:
			clients.append(address)

		cctime = time.strftime("%H:%M:%S %d-%m-%Y", time.localtime())

		print("IP:["+address[0]+"] Port:["+str(address[1])+"] Time:["+cctime+"] Name:", end="")
		print(message.decode("utf-8"))

		for client in clients:
			if address != client:
				s.sendto(message, client)

	except:
		print("Server stopped")
		quit = True

s.close()
