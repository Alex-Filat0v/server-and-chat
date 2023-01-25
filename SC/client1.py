from PyQt5 import QtWidgets, uic
import sys
import pickle
import random
import math
import rsa
import socket
import threading
import time

key = 78
shutdown = False
joinc = False

def receving(name, sock):
	while not shutdown:
		try:
			while True:
				message, address = s.recvfrom(1024)
				decrypt = ""; k =False
				for i in message.decode("utf-8"):
					if i == ":":
						k = True
						decrypt += i
					elif k == False or i == " ":
						decrypt += i 
					else:
						decrypt += chr(ord(i)^key)
				print(decrypt)
				time.sleep(0.2)
		except:
			pass

host = socket.gethostbyname(socket.gethostname())
port = 0
server = (socket.gethostbyname(socket.gethostname()), 9090)
server = ("26.82.194.252", 9090)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)
alias = input("Name: ")

rT = threading.Thread(target = receving, args = ("RecvThread", s))
rT.start()

while shutdown == False:
	if joinc == False:
		s.sendto(("["+alias + "] join chat ").encode("utf-8"), server)
		joinc = True
	else:
		try:
			message = input()
			crypt = ""
			for i in message:
				crypt += chr(ord(i)^key)
			message = crypt
			if message != "":
				s.sendto(("["+alias + "] say: "+message).encode("utf-8"), server)
			time.sleep(0.2)
		except:
			s.sendto(("["+alias + "] left chat ").encode("utf-8"), server)
			shutdown = True

rT.join()
s.close()
