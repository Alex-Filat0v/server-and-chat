T = True
opnum1 = 73
opnum2 = 29
yclkey = 1

send_yuser_name = input(str("Напишите имя пользователя, которому вы хотите написать: "))

sv = open ("FL.txt", "r")
check_yser_name = (sv.read())
sv.close()

if send_yuser_name == check_yser_name:
	print("right name")
	T = True
else:
	print("uncorrect name")
	T = False

if T == True:
	input(str("Введите ваше сообщение: "))
else:
	print("uncorrect name")


sv = open ("yclkey.txt", "r")
yclkey = (sv.read())
sv.close()

input ("nothing")
