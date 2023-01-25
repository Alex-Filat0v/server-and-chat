import socket
import sqlite3
import uuid
from threading import Thread
import time


def incomming_connection():
	while True:
		client, adress = server.accept()
		Thread(target=single_client, args=(client,)).start()


def single_client(client):
	database = sqlite3.connect('person.db')
	cursor = database.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS persons (
		"pid"	INTEGER NOT NULL UNIQUE,
		"login"	TEXT NOT NULL UNIQUE,
		"password"	TEXT NOT NULL,
		"token" TEXT,
		PRIMARY KEY("pid")
	) """)
	database.commit()

	while True:
		data = client.recv(2048)
		check = data.decode("utf-8")

		if check == "FirstRegistration":
			data = client.recv(2048)
			check = data.decode("utf-8")
			plogin = check
			cursor.execute(f"""SELECT login FROM persons  WHERE login = '{plogin}' """)
			if cursor.fetchone() is None:
				client.send("PSS".encode("utf-8"))
				data = client.recv(2048)
				pps1 = data.decode("utf-8")
				data = client.recv(2048)
				pps2 = data.decode("utf-8")
				if pps1 == pps2:
					ppassword = pps2
					cursor.execute(f"""INSERT INTO persons ("login", "password") VALUES (?, ?)""", (plogin, ppassword))
					database.commit()
					cursor.execute(f"""SELECT pid FROM persons  WHERE login = '{plogin}' """)
					t = cursor.fetchone()
					database.commit()
					t = str(t)
					t = t[1:-2]
					random_hash = uuid.uuid4()
					token = t + str(random_hash) + t
					cursor.execute(f"""UPDATE persons SET token = '{token}' WHERE pid = '{t}' AND login = '{plogin}' """)
					database.commit()
					# print(f"Пользователь {check} зарегестрировался")
					client.send("SUCCESS".encode("utf-8"))
					token = str(token)
					client.send(token.encode("utf-8"))
					clients[client]=plogin
					pass
				else:
					client.send("UNSUCCESS".encode("utf-8"))
					pass
			else:
				client.send("UNSUCCESS".encode("utf-8"))
				pass

		elif check == "CheckName":
			data = client.recv(2048)
			name = data.decode("utf-8")
			data = client.recv(2048)
			checkpass = data.decode("utf-8")
			cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{name}' AND password = '{checkpass}' """)
			if cursor.fetchone() is None:
				client.send("U".encode("utf-8"))
				pass
			else:
				cursor.execute(f"""SELECT pid FROM persons  WHERE login = '{name}' """)
				t = cursor.fetchone()
				database.commit()
				t = str(t)
				t = t[1:-2]
				random_hash = uuid.uuid4()
				token = t + str(random_hash) + t
				cursor.execute(f"""UPDATE persons SET token = '{token}' WHERE pid = '{t}' AND login = '{name}' """)
				database.commit()
				token = str(token)
				# print(f"Пользователь {name} зашел")
				client.send(token.encode("utf-8"))
				clients[client]=name
				pass
			pass

		elif check == "ChangeUName":
			data = client.recv(2048)
			check = data.decode("utf-8")
			pas1 = check
			data = client.recv(2048)
			check = data.decode("utf-8")
			pas2 = check
			if pas1 == pas2:
				cursor.execute(f"""SELECT login, password FROM persons WHERE login = '{clients[client]}' AND password = '{pas2}' """)
				if cursor.fetchone() is None:
					client.send("CANTSELECTP".encode("utf-8"))
					pass
				else:
					client.send("PSS".encode("utf-8"))
					data = client.recv(2048)
					check = data.decode("utf-8")
					rename = check
					cursor.execute(f"""SELECT login FROM persons WHERE login = '{rename}' """)
					if cursor.fetchone() is None:
						client.send("NA".encode("utf-8"))
						cursor.execute(f"""UPDATE persons SET login = '{rename}' WHERE login = '{clients[client]}' """)
						database.commit()
						clients[client] = rename
						pass
					else:
						client.send("NNA".encode("utf-8"))
						pass
			else:
				pass

		elif check == "MyPid":
			data = client.recv(2048)
			check = data.decode("utf-8")
			tok = check
			data = client.recv(2048)
			check = data.decode("utf-8")
			if check == 'not':
				pass
			else:
				data = client.recv(2048)
				check = data.decode("utf-8")
				person_password = check
				cursor.execute(f"""SELECT token, password FROM persons WHERE token = '{tok}' AND password = '{person_password}' """)
				if cursor.fetchone() is None:
					client.send("none".encode('utf-8'))
					pass
				else:
					for value1 in cursor.execute(f"""SELECT pid FROM persons WHERE token = '{tok}' AND password = '{person_password}'"""):
						value1 = str(value1)
						value1 = value1[1:-2]
						client.send(value1.encode("utf-8"))
						pass
					pass
				pass

		elif check == "ChangeUPass":
			data = client.recv(2048)
			check = data.decode("utf-8")
			tok = check
			data = client.recv(2048)
			check = data.decode("utf-8")
			pas1 = check
			data = client.recv(2048)
			check = data.decode("utf-8")
			pas2 = check
			if pas1 == pas2:
				cursor.execute(f"""SELECT token, password FROM persons WHERE token = '{tok}' AND password = '{pas2}' """)
				if cursor.fetchone() is None:
					client.send("CANTSELECTP".encode("utf-8"))
					pass
				else:
					client.send("PSS".encode("utf-8"))
					data = client.recv(2048)
					check = data.decode("utf-8")
					newpass = check
					if newpass == pas2:
						client.send("NAI".encode("utf-8"))
						pass
					else:
						client.send("OK".encode("utf-8"))
						data = client.recv(2048)
						check = data.decode("utf-8")
						check_id = check
						cursor.execute(f"""SELECT pid, token, password FROM persons WHERE pid = '{check_id}' AND token = '{tok}' AND password = '{pas2}' """)
						if cursor.fetchone() is None:
							client.send("NAI".encode("utf-8"))
							pass
						else:
							client.send("KOK".encode("utf-8"))
							cursor.execute(f"""UPDATE persons SET password = '{newpass}' WHERE pid = '{check_id}' AND token = '{tok}' AND password = '{pas2}' """)
							database.commit()
							pass
			else:
				pass

		elif check == "AddUFriend":
			cursor.execute("""CREATE TABLE IF NOT EXISTS friends (
				logins_who_adds_the_friends TEXT,
				logins_who_added_as_a_friendd TEXT
			) """)
			database.commit()
			data = client.recv(2048)
			check = data.decode("utf-8")
			new_friend = check
			data = client.recv(2048)
			check = data.decode("utf-8")
			new_friend_id = check
			cursor.execute(f"""SELECT pid, login FROM persons WHERE pid = '{new_friend_id}' AND login = '{new_friend}'""")
			if cursor.fetchone() is None:
				client.send("NET".encode("utf-8"))
				pass
			else:
				client.send("KOK".encode("utf-8"))
				cursor.execute(f"""SELECT logins_who_adds_the_friends, logins_who_added_as_a_friendd FROM friends WHERE logins_who_adds_the_friends = '{clients[client]}' AND logins_who_added_as_a_friendd = '{new_friend}' """)
				if cursor.fetchone() is None:
					cursor.execute(f"""INSERT INTO friends VALUES (?, ?)""", (clients[client], new_friend))
					database.commit()
					client.send("KOK".encode("utf-8"))
					pass
				else:
					client.send("NOK".encode("utf-8"))
					pass
				pass

		elif check == "NewMessage":
			cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
				id INTEGER NOT NULL UNIQUE,
				pfrom TEXT,
				pto TEXT,
				message TEXT,
				PRIMARY KEY(id)
			) """)
			
			data = client.recv(2048)
			check = data.decode("utf-8")
			FM = check
			cursor.execute(f"""SELECT logins_who_adds_the_friends, logins_who_added_as_a_friendd FROM friends WHERE logins_who_adds_the_friends = '{clients[client]}' AND logins_who_added_as_a_friendd = '{FM}' """)
			if cursor.fetchone() is None:
				client.send("NOT UR FRIEND".encode("utf-8")) 
				pass
			else:
				client.send("2nd test".encode("utf-8"))
				cursor.execute(f"""SELECT logins_who_adds_the_friends, logins_who_added_as_a_friendd FROM friends WHERE logins_who_adds_the_friends = '{FM}' AND logins_who_added_as_a_friendd = '{clients[client]}' """)
				if cursor.fetchone() is None:
					client.send("NOT FRIEND".encode("utf-8"))
					pass
				else:
					client.send("FRIEND".encode("utf-8"))
					data = client.recv(2147483647)
					check = data.decode("utf-8")
					umessage = check
					cursor.execute(f"""INSERT INTO messages ("pfrom", "pto", "message") VALUES (?, ?, ?)""", (clients[client], FM, umessage))
					database.commit()
					pass
				pass
			pass

		elif check == "ShowMessage":
			data = client.recv(2048)
			check = data.decode("utf-8")
			FM = check
			cursor.execute(f"""SELECT id, pfrom, message FROM messages	WHERE (pfrom = '{clients[client]}' AND pto = '{FM}') OR (pfrom = '{FM}' AND pto = '{clients[client]}') """)
			all_msg = cursor.fetchall()
			client.send(str(len(all_msg)).encode('utf-8'))
			if len(all_msg) > 0:	
				for i in range(len(all_msg)):
					pfrom = all_msg[i][1]
					msg = all_msg[i][2]
					message = f"{pfrom}: {msg}"
					client.send(message.encode("utf-8"))
					time.sleep(0.00001)

		elif check == "Update":
			cursor.execute(f"""SELECT logins_who_added_as_a_friendd FROM friends WHERE logins_who_adds_the_friends = '{clients[client]}' """)
			all_fr = cursor.fetchall()
			client.send(str(len(all_fr)).encode('utf-8'))
			time.sleep(0.1)
			if len(all_fr) > 0:
				for i in range(len(all_fr)):
					time.sleep(0.01)
					fr = str(all_fr[i][0])
					client.send(fr.encode('utf-8'))
					time.sleep(0.01)

		elif check == "logout":
			cursor.execute(f"""UPDATE persons SET token = '{None}' WHERE login = '{clients[client]}'  """)
			database.commit()
			del clients[client]

		elif check == "exit":
			if clients.get(client):
				cursor.execute(f"""UPDATE persons SET token = '{None}' WHERE login = '{clients[client]}'  """)
				database.commit()
				del clients[client]
			client.close()	
			break

		elif check == "show_all_people":
			cursor.execute(f"""SELECT login FROM persons WHERE token <> '{None}' """)
			all_persons = cursor.fetchall()
			client.send(str(len(all_persons)).encode('utf-8'))
			time.sleep(0.1)
			if len(all_persons) > 0:
				for i in range(len(all_persons)):
					time.sleep(0.01)
					fr = str(all_persons[i][0])
					client.send(fr.encode('utf-8'))
					time.sleep(0.01)


if __name__ == "__main__":
	clients = {}

	server_ip = "localhost"
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((server_ip, 1245))
	server.listen(10)
	print("server работает!")

	global database
	global cursor

	accert_thread = Thread(target=incomming_connection)
	accert_thread.start()
	accert_thread.join()
	server.close()
