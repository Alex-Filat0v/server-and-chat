import sqlite3
import random

database = sqlite3.connect('T1.db')
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS persons (
	pid INT,
	login TEXT,
	password TEXT
) """)
database.commit()

database = sqlite3.connect('T2.db')
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS friends (
	pid INT,
	login1 TEXT,
	login2 TEXT
) """)
database.commit()

pid = int(random.uniform(0, 2147483648))
plogin = input("login: ")
ppassword = input("password: ")

cursor.execute(f"""SELECT login FROM persons WHERE login = '{plogin}' """)
if cursor.fetchone() is None:
	cursor.execute(f"""INSERT INTO persons VALUES (?, ?, ?)""", (pid, plogin, ppassword))
	database.commit()
	print("Запись создана")
else:
	print("Уже есть запись")
	for value in cursor.execute("SELECT * FROM persons"):
		print(value)

pid = int(random.uniform(0, 2147483648))
login1 = input("login: ")
login2 = input("password: ")

cursor.execute(f"""SELECT login FROM friends WHERE login = '{login1}' """)
if cursor.fetchone() is None:
	cursor.execute(f"""INSERT INTO persons VALUES (?, ?, ?)""", (pid, login1, login2))
	database.commit()
	print("Запись создана")
else:
	print("Уже есть запись")
	for value in cursor.execute("SELECT * FROM persons"):
		print(value)
