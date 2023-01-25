import random
import sqlite3

database = sqlite3.connect('person123.db')
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS persons (
	pid INT,
	login TEXT,
	password TEXT
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

input()
