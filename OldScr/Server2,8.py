#Тута я импортирую библиотеки разные
import random
import socket
import sqlite3

#Запуск сервера
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost", 1234))
server.listen(10)
print("server is working")

#Создание базы данных
global database
global cursor

database = sqlite3.connect('person.db')
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS persons (
	pid INT,
	login TEXT,
	password TEXT
) """)
database.commit()


#Пока что бесконечная функция прослушки клиента
while True:
	#Ждем подключение клиента для его обработки
	user_socket, adress = server.accept()
	print(f"user {adress} connected!")
	Tbun = True

	while True:
		#Слушаем команду от клиента
		data = user_socket.recv(2048)
		check = data.decode("utf-8")

#!!!
		if check == "FirstRegistration":
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			pid = int(random.uniform(0, 2147483648))
			plogin = check
			cursor.execute(f"""SELECT login FROM persons WHERE login = '{plogin}' """)
			if cursor.fetchone() is None:
				user_socket.send("PSS".encode("utf-8"))
				data = user_socket.recv(2048)
				pps1 = data.decode("utf-8")
				data = user_socket.recv(2048)
				pps2 = data.decode("utf-8")
				if pps1 == pps2:
					ppassword = pps2
					cursor.execute(f"""INSERT INTO persons VALUES (?, ?, ?)""", (pid, plogin, ppassword))
					database.commit()
					print(f"Пользователь {check} зарегестрировался")
					user_socket.send("SUCCESS".encode("utf-8"))
					pass
				else:
					user_socket.send("UNSUCCESS".encode("utf-8"))
					pass
			else:
				user_socket.send("UNSUCCESS".encode("utf-8"))
				pass

#!!!
		elif check == "CheckName":
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			user_socket.send("CheckPass".encode("utf-8"))
			data = user_socket.recv(2048)
			checkpass = data.decode("utf-8")
			cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{check}' AND password = '{checkpass}' """)
			if cursor.fetchone() is None:
				user_socket.send("U".encode("utf-8"))
				print("Пользователь не смог пройти проверку")
				pass
			else:
				user_socket.send(f"С возвращением {check}".encode("utf-8"))
				print(f"Пользователь {check} зашел")
				for value in cursor.execute(f"""SELECT pid, login, password FROM persons WHERE login = '{check}' AND password = '{checkpass}'"""):
			#		print(value)
					pass
				pass
			pass

#!!!
		elif check == "ChangeUName":
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			log = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			pas1 = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			pas2 = check
			if pas1 == pas2:
				cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{log}' AND password = '{pas2}' """)
				if cursor.fetchone() is None:
					user_socket.send("CANTSELECTP".encode("utf-8"))
					pass
				else:
					user_socket.send("PSS".encode("utf-8"))
					data = user_socket.recv(2048)
					check = data.decode("utf-8")
					newname = check
					cursor.execute(f"""SELECT login FROM persons WHERE login = '{newname}' """)
					if cursor.fetchone() is None:
						user_socket.send("NA".encode("utf-8"))
						data = user_socket.recv(2048)
						check = data.decode("utf-8")
						car = check
						if car == pas2:
							cursor.execute(f"""UPDATE persons SET login = '{newname}' WHERE login = '{log}' AND password = '{pas2}' """)
							database.commit()
							pass
						else:
							pass
					else:
						user_socket.send("NNA".encode("utf-8"))
						pass
			else:
				pass

#!!!
		elif check == "MyPid":
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			plogin = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			ppassword = check
			cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{plogin}' AND password = '{ppassword}' """)
			if cursor.fetchone() is None:
				user_socket.send("not".encode('utf-8'))
				pass
			else:
				for value1 in cursor.execute(f"""SELECT pid FROM persons WHERE login = '{plogin}' AND password = '{ppassword}'"""):
					value1 = str(value1)
					value1 = value1[1:-2]
					user_socket.send(value1.encode("utf-8"))
					pass
				pass
			pass

#!!!
		elif check == "ChangeUPass":
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			log = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			pas1 = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			pas2 = check
			if pas1 == pas2:
				cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{log}' AND password = '{pas2}' """)
				if cursor.fetchone() is None:
					user_socket.send("CANTSELECTP".encode("utf-8"))
					pass
				else:
					user_socket.send("PSS".encode("utf-8"))
					data = user_socket.recv(2048)
					check = data.decode("utf-8")
					newpass = check
					data = user_socket.recv(2048)
					check = data.decode("utf-8")
					check1p = check
					if check1p == pas2:
						data = user_socket.recv(2048)
						check = data.decode("utf-8")
						check2i = check
						cursor.execute(f"""SELECT pid, login, password FROM persons WHERE pid = '{check2i}' AND login = '{log}' AND password = '{check1p}' """)
						if cursor.fetchone() is None:
							user_socket.send("NAI".encode("utf-8"))
							pass
						else:
							user_socket.send("KOK".encode("utf-8"))
							cursor.execute(f"""UPDATE persons SET password = '{newpass}' WHERE pid = '{check2i}' AND login = '{log}' AND password = '{check1p}' """)
							database.commit()
							pass
					else:
						pass
			else:
				pass

#!!!
		elif check == "AddUFriend":
			cursor.execute("""CREATE TABLE IF NOT EXISTS friends (
				logins_who_adds_the_friends TEXT,
				logins_who_added_as_a_friendd TEXT
			) """)
			database.commit()
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			YN = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			YP = check
			cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{YN}' AND password = '{YP}' """)
			if cursor.fetchone() is None:
				user_socket.send("NOPE".encode("utf-8"))
				pass
			else:
				user_socket.send("KOK".encode("utf-8"))
				data = user_socket.recv(2048)
				check = data.decode("utf-8")
				NF = check
				data = user_socket.recv(2048)
				check = data.decode("utf-8")
				NFID = check
				cursor.execute(f"""SELECT pid, login FROM persons WHERE pid = '{NFID}' AND login = '{NF}'""")
				if cursor.fetchone() is None:
					user_socket.send("NET".encode("utf-8"))
					pass
				else:
					user_socket.send("KOK".encode("utf-8"))
					cursor.execute(f"""SELECT logins_who_adds_the_friends, logins_who_added_as_a_friendd FROM friends WHERE logins_who_adds_the_friends = '{YN}' AND logins_who_added_as_a_friendd = '{NF}' """)
					if cursor.fetchone() is None:
						cursor.execute(f"""INSERT INTO friends VALUES (?, ?)""", (YN, NF))
						database.commit()
						user_socket.send("KOK".encode("utf-8"))
						pass
					else:
						user_socket.send("NOK".encode("utf-8"))
						pass
					pass
				pass

#!!!
		elif check == "NewMessage":
			cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
				pfrom TEXT,
				pto TEXT,
				message TEXT
			) """)
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			PN = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			PP = check
			cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{PN}' AND password = '{PP}' """)
			if cursor.fetchone() is None:
				user_socket.send("NOPE".encode("utf-8"))
				pass
			else:
				user_socket.send("KOK".encode("utf-8"))
				data = user_socket.recv(2048)
				check = data.decode("utf-8")
				FM = check
				cursor.execute(f"""SELECT logins_who_adds_the_friends, logins_who_added_as_a_friendd FROM friends WHERE logins_who_adds_the_friends = '{PN}' AND logins_who_added_as_a_friendd = '{FM}' """)
				if cursor.fetchone() is None:
					user_socket.send("NOT UR FRIEND".encode("utf-8")) 
					pass
				else:
					user_socket.send("2nd test".encode("utf-8"))
					cursor.execute(f"""SELECT logins_who_adds_the_friends, logins_who_added_as_a_friendd FROM friends WHERE logins_who_adds_the_friends = '{FM}' AND logins_who_added_as_a_friendd = '{PN}' """)
					if cursor.fetchone() is None:
						user_socket.send("NOT FRIEND".encode("utf-8"))
						pass
					else:
						user_socket.send("FRIEND".encode("utf-8"))
						data = user_socket.recv(2147483647)
						check = data.decode("utf-8")
						umessage = check
						cursor.execute(f"""INSERT INTO messages VALUES (?, ?, ?)""", (PN, FM, umessage))
						database.commit()
						pass
					pass
				pass

#!!!
		elif check == "UHaveNewMessage":
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			PN = check
			data = user_socket.recv(2048)
			check = data.decode("utf-8")
			PP = check
			cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{PN}' AND password = '{PP}' """)
			if cursor.fetchone() is None:
				user_socket.send("NOPE".encode("utf-8"))
				pass
			else:
				#Нужно подумать что делать если нет сообщений!!!
				user_socket.send("KOK".encode("utf-8"))
				for value1 in cursor.execute(f"""SELECT pfrom, message FROM messages WHERE pto = '{PN}'"""):
					if cursor.fetchone() is None:
						user_socket.send("NO MESSAGES".encode("utf-8"))
						pass
					else:
						user_socket.send("MESSAGES".encode("utf-8"))
						value1 = str(value1)
						user_socket.send(value1.encode("utf-8"))
						pass
				pass


#		Tbun = False
