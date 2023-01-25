import sqlite3
import random

database = sqlite3.connect('iterM.db')
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS test (
	nump INT,
	pidt INT,
	boo INT
) """)
database.commit()

bak = 1
bo = 0

print("Working: ")

for i in range(1000000):
	bo = 0
	pid = int(random.uniform(0, 2147483648))
	cursor.execute(f"""SELECT * FROM test WHERE pidt = '{pid}' """)
	if cursor.fetchone() is None:
		cursor.execute(f"""INSERT INTO test VALUES (?, ?, ?)""", (bak, pid, bo))
		database.commit()
		bak += 1
		#print(f"Число {pid} Занесено в таблицу")
	else:
		bo = 1
		cursor.execute(f"""INSERT INTO test VALUES (?, ?, ?)""", (bak, pid, bo))
		print(f"Число {pid} встретилось снова!!!")
		print(f"Число встретилось вновь на {bak} итерации")
		database.commit()
		bak += 1


input("Press 'ENTER' to continue")
