#Тута я импортирую библиотеки разные
import socket
import os

#А вот тут я задаю разные функции
#Функция присваивания имени при первом входе
def FirstRegistration():
	client.send("FirstRegistration".encode("utf-8"))
	user_name = str(input("Введите желаемое имя пользователя: "))
	client.send(user_name.encode("utf-8"))
	data = client.recv(2048)
	data = data.decode("utf-8")
	if data == "PSS":
		user_password = str(input("Введите свой пароль:"))
		client.send(user_password.encode("utf-8"))
		os.system('cls')
		user_password2 = str(input("Повторите свой пароль:"))
		client.send(user_password2.encode("utf-8"))
		os.system('cls')
		data = client.recv(2048)
		data = data.decode("utf-8")
		if data == "SUCCESS":
			print(f"Вы успешно зарегестрировались, добро пожаловать {user_name}")
			Mainmenyoo()
		else:
			print("Пароли не совпадают, попробуйте зарегестрироваться еще раз")
			MainStart()
	else:
		os.system('cls')
		print("Такое имя уже существует, выберите себе другое")
		FirstRegistration()
#Добавления друга	
#!!!
def AddUFriend():
	client.send("AddUFriend".encode("utf-8"))
	os.system('cls')
	YN = str(input("Введите свой ник: "))
	client.send(YN.encode('utf-8'))
	YP = str(input("Введите свой пароль: "))
	client.send(YP.encode('utf-8'))
	data = client.recv(2048)
	data = data.decode("utf-8")
	if data == "NOPE":
		os.system('cls')
		print("Не правильно введен логин или пароль, повторите попытку")
		Mainmenyoo()
	else:
		os.system('cls')
		NF = str(input("Введите имя своего друга, для добавления его в список друзей: "))
		client.send(NF.encode('utf-8'))
		NFID = str(input("Введите ID своего друга: "))
		client.send(NFID.encode('utf-8'))
		data = client.recv(2048)
		data = data.decode("utf-8")
		if data == "KOK":
			data = client.recv(2048)
			data = data.decode("utf-8")
			if data == "KOK":
				os.system('cls')
				print(f"Теперь {NF} является вашим другом")
				Mainmenyoo()
			else:
				os.system('cls')
				print(f"{NF} уже является вашим другом")
				Mainmenyoo()
		else:
			os.system('cls')
			print("Не правильно введен ник или ID друга, повторите попытку")
			Mainmenyoo()
#Отправка сообщений
#!!!
def NewMessage():
	client.send("NewMessage".encode("utf-8"))
	os.system('cls')
	YN = str(input("Введите свой ник: "))
	client.send(YN.encode('utf-8'))
	YP = str(input("Введите свой пароль: "))
	client.send(YP.encode('utf-8'))
	data = client.recv(2048)
	data = data.decode("utf-8")
	if data != "KOK":
		os.system('cls')
		print("Не правильно введен логин или пароль, повторите попытку")
		Mainmenyoo()
	else:
		os.system('cls')
		FM = str(input("Введите имя своего друга, которому вы хотите написать: "))
		client.send(FM.encode('utf-8'))
		data = client.recv(2048)
		data = data.decode("utf-8")
		if data == "NOT UR FRIEND":
			os.system('cls')
			print("Этого пользователя нет в вашем списке друзей")
			Mainmenyoo()
		elif data == "2nd test":
			data = client.recv(2048)
			data = data.decode("utf-8")
			if data == "NOT FRIEND":
				os.system('cls')
				print("Данный пользователь не добавил вас в список друзей, пока он вас не добавит в свой список друзей, вы не можете отправлять ему сообщения")
				Mainmenyoo()
			elif data == "FRIEND":
				os.system('cls')
				urmessage = str(input(f"Введите ваше сообщение пользователю {FM}: "))
				client.send(urmessage.encode('utf-8'))
				os.system('cls')
				print("Ваше сообщение было успешно отправленно!")
				Mainmenyoo()
#Главное меню
#!!!
def Mainmenyoo():
	print("")
	print("Вот список доступных команд:")
	print("1.Добавить человека в список друзей")
	print("2.Написать сообщение")
	print("3.Посмотреть мои сообщения")
	print("4.Изменить свой ник")
	print("5.Изменить свой пароль")
	print("6.Узнато мой id (он необходим для смены пароля)")
	print("")
	variant1 = int(input("Выберите одну из этих команду (писать нужно строго цифры!!!): "))
	if variant1 == 1:
		AddUFriend()
	elif variant1 == 2:
		NewMessage()
	elif variant1 == 3:
		UHaveNewMessage()
	elif variant1 == 4:
		ChangeUName()
	elif variant1 == 5:
		ChangeUPass()
	elif variant1 == 6:
		MyPid()
	else:
		os.system('cls')
		print("Шо то ты не то написал")
		print("")
		Mainmenyoo()
#Смена ника
#!!!
def ChangeUName():
	client.send("ChangeUName".encode("utf-8"))
	print("")
	log1 = str(input("Введите свой логин: "))
	client.send(log1.encode("utf-8"))
	pas1 = str(input("Введите свой пароль: "))
	client.send(pas1.encode("utf-8"))
	os.system('cls')
	pas2 = str(input("Повторите совй пароль: "))
	client.send(pas2.encode("utf-8"))
	if pas1 != pas2:
		os.system('cls')
		print("Введенные вами пароли не совпадают, повторите попытку снова")
		Mainmenyoo()
	else:
		data = client.recv(2048)
		data = data.decode("utf-8")
		if data == "PSS":
			os.system('cls')
			newname = str(input("Введите свое новое имя: "))
			client.send(newname.encode('utf-8'))
			data = client.recv(2048)
			data = data.decode("utf-8")
			if data == "NA":
				print(f"Вы точно уверены что хотите сменить ник {log1} на {newname} ???")
				acce = input(str("Для подтверждения еще раз введите пароль: "))
				client.send(acce.encode('utf-8'))
				if acce == pas2:
					os.system('cls')
					print(f"Ник был успешно изменен теперь вы {newname}, не забудьте об этом, когда будите входить в следующий раз!")
					Mainmenyoo()					
				else:
					os.system('cls')
					print("Ник не был изменен, возвращаю вас в главное меню")
					Mainmenyoo()
			else:
				os.system('cls')
				print("Пользователь с таким именем уже существует, выберите себе другое")
				Mainmenyoo()
		else:
			os.system('cls')
			print("Не правильно введен логин или пароль, повторите попытку")
			Mainmenyoo()
#Смена пароля
#!!!
def ChangeUPass():
	client.send("ChangeUPass".encode('utf-8'))
	print("")
	log1 = str(input("Введите свой логин: "))
	client.send(log1.encode("utf-8"))
	pas1 = str(input("Введите свой пароль: "))
	client.send(pas1.encode("utf-8"))
	os.system('cls')
	pas2 = str(input("Повторите совй пароль: "))
	client.send(pas2.encode("utf-8"))
	if pas1 != pas2:
		os.system('cls')
		print("Введенные вами пароли не совпадают, повторите попытку снова")
		Mainmenyoo()
	else:
		data = client.recv(2048)
		data = data.decode("utf-8")
		if data == "PSS":
			os.system('cls')
			newpass = str(input("Введите свой новый пароль: "))
			os.system('cls')
			client.send(newpass.encode('utf-8'))
			print(f"Вы точно уверены что хотите сменить пароль на {newpass} ???")
			acce = str(input("Для подтверждения еще раз введите пароль: "))
			client.send(acce.encode('utf-8'))
			if acce == pas2:
				os.system('cls')
				acce = str(input("Для подтверждения введите свой ID: "))
				client.send(acce.encode('utf-8'))
				data = client.recv(2048)
				data = data.decode("utf-8")
				if data == "KOK":
					os.system('cls')
					print(f"Пароль был успешно изменен, не забудьте об этом, когда будите входить в следующий раз!")
					Mainmenyoo()
				else:
					os.system('cls')
					print(f"Пароль не был изменен, не верно введен ID")
					Mainmenyoo()
			else:
				os.system('cls')
				print("Пароль не был изменен, возвращаю вас в главное меню")
				Mainmenyoo()
		else:
			os.system('cls')
			print("Не правильно введен логин или пароль, повторите попытку")
			Mainmenyoo()
#Проверка наличия новых сообщений
#!!!
def UHaveNewMessage():
	client.send("UHaveNewMessage".encode('utf-8'))
	os.system('cls')
	YN = str(input("Введите свой ник: "))
	client.send(YN.encode('utf-8'))
	YP = str(input("Введите свой пароль: "))
	client.send(YP.encode('utf-8'))
	data = client.recv(2048)
	data = data.decode("utf-8")
	if data != "KOK":
		os.system('cls')
		print("Не правильно введен логин или пароль, повторите попытку")
		Mainmenyoo()
	else:
		#Нужно подумать что делать если нет сообщений!!!
		os.system('cls')
		data = client.recv(2147483648)
		data = data.decode("utf-8")
		print(f"Ваши входящие сообщения: {data}")
		v = input("Для возвращения в главное меню введите любое число: ")
		if v == "1":
			os.system('cls')
			Mainmenyoo()
		else:
			os.system('cls')
			Mainmenyoo()
#Проверка логина и пароля при входе
#!!!
def Log_in():
	client.send("CheckName".encode("utf-8"))
	check = input("Введите свое имя: ")
	client.send(check.encode("utf-8"))
	data = client.recv(2048)
	data = data.decode("utf-8")
	if data == "CheckPass":
		check = input("Введите свой пароль: ")
		client.send(check.encode("utf-8"))
		data = client.recv(2048)
		data = data.decode("utf-8")
		os.system('cls')
		if data == "U":
			vib = input("Не верно указан логин или пароль, для того что бы попробовать снова введите 1, для регистрации введите 2: ")
			if vib == "1":
				Log_in()
			else:
				FirstRegistration()
		else:
			os.system('cls')
			print(data)
			Mainmenyoo()
#Войти или зарегестрироваться
#!!!
def MainStart():
	vib = input("Для входа введите 1, а для регистрации 2: ")
	if vib == "1":
		Log_in()
	elif vib == "2":
		FirstRegistration()
#Узнать мой ID
#!!!
def MyPid():
	client.send("MyPid".encode("utf-8"))
	msen = input("Введите свой логин: ")
	client.send(msen.encode('utf-8'))
	msen = input("Введите свой пароль: ")
	client.send(msen.encode('utf-8'))
	data = client.recv(2048)
	data = data.decode("utf-8")
	if data != "not":
		os.system('cls')
		print(f"Ваш ID:{data}")
		Mainmenyoo()
	else:
		os.system('cls')
		print("Не верно введен логин или пароль, повторите попытку")
		Mainmenyoo()


#Для общения с сервером
global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 1234))
Tbun = True


#Тут мы вызываем функцию входи или регистрации
MainStart()


#Приветствие при каждом старте 
print("")
print("		 Привет!")
print("	Это абсолютно анонимный чат")
print("тут ты можешь писать кому хочешь и что хочешь!")
print("		 Начнём!")



#ПРИ НОРМАЛЬНОЙ РАБОТЕ ЭТО СООБЩЕНИЕ НЕ ДОЛЖНО ПОЯВЛЯТЬСЯ !!!
input("Press 'ENTER' to continue")
