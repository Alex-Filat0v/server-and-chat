#А вот тут я задаю разные функции
#Функция присваивания имени при первом входе
def FirstRegistration():
	user_name = input(str("Введите желаемое имя пользователя: "))
	sv = open ("name.txt", "x")
	sv.write (user_name)
	sv.close()

#Добавления друга
def AddUFriend():
	FN = input("Введите имя своего друга, для добавления его в список контактов: ")
	try:
		sv = open ("FL.txt", "a")
		sv.write (FN)
		sv.close()
		print("")
		print("Друг "+FN+" был добавлен в ваш список друзей")
		print("")
		print("Возвращаю вас в главное меню")
		Mainmenyoo()
	except FileNotFoundError:
		file = open("FL.txt", "w")
		file.write(FN)
		file.close()
		print("")
		print("Друг "+FN+" был добавлен в ваш список друзей")
		print("")
		print("Возвращаю вас в главное меню")
		Mainmenyoo()

#Отправка сообщений
def ChooseUFriend():
	send_user_name = input(str("Напишите имя пользователя, которому вы хотите написать: "))
	#file = open("name.txt", "r")
	#PN1 = file.read()
	#file.close()
	try:
		sv = open ("FL.txt", "r")
		check_user_name = (sv.read())
		sv.close()
	except FileNotFoundError:
		print("")
		print("У вас никого нет в списке друзей(((")
		print("Возвращаю вас в главное меню")
		print("")
		Mainmenyoo()
	if send_user_name == check_user_name:
		message = input(str("Введите ваше сообщение: "))
		file = open("message_to_"+check_user_name+".txt", "w") #"|"+PN1+
		#Хз чо делать, но нужно заменить способ записи и добавить возможность чтения на сервер и клиенту!!!
		file.write(message)
		file.close()
		print("")
		print("Сообщение было успешно отправленно")
		print("Возвращаю вас в главное меню")
		Mainmenyoo()
	else:
		print("У вас нет этого человека в списке друзей")
		vib = int(input("Если хотите заново ввести имя друга напишите '1', если хотите вернутся в главное меню напишите '2': "))
		if vib == 1:
			ChooseUFriend()
		elif vib == 2:
			print("")
			print("Возвращаю вас в главное меню")
			Mainmenyoo()

#Главное меню
def Mainmenyoo():
	print("")
	print("Вот список доступных команд:")
	print("1.Добавить человека в список друзей")
	print("2.Написать сообщение")
	print("3.Изменить свой ник")
	print("")
	variant1 = int(input("Выберите одну из этих команду (писать нужно строго одну цифру!!!): "))
	if variant1 == 1:
		AddUFriend()
	elif variant1 == 2:
		ChooseUFriend()
	elif variant1 == 3:
		ChangeUName()
	else:
		print("Шо то ты не то написал")
		print("")
		Mainmenyoo()

#Смена ника
def ChangeUName():
	print("")
	file = open ("name.txt", "r")
	print("Твой старый ник:", file.read())
	file.close()
	user_name = input("Введите новое имя пользователя: ")
	print("")
	print("Вы уверены что хотите сменить совй ник ?")
	agree = str(input("Для подтверждения напишите 'Yes!' : "))
	print("")
	if agree == 'Yes!':
		sv = open ("name.txt", "w")
		sv.write (user_name)
		sv.close()
		file = open ("name.txt", "r")
		print("Готово, твой ник был изменен, теперь ты:", file.read())
		file.close()
		print("")
		print("Возвращаю вас в главное меню")
		Mainmenyoo()
	else:
		print("Вы не прошли подтверждение!!!")
		print("")
		print("Возвращаю вас в главное меню")
		Mainmenyoo()

#Проверка наличия новых сообщений
def UHaveNewMessage():
	file = open("name.txt", "r")
	yourname = file.read()
	file.close()
	try:
		file = open("message_to_"+yourname+".txt", "r") #"|"+PN1+
		print("")
		print("У вас новое сообщение: "+file.read())
		Mainmenyoo()
	except FileNotFoundError:
		print("")
		print("У вас нет новых сообщений")
		Mainmenyoo()


#Приветствие при каждом старте 
print("		 Привет!")
print("	Это абсолютно анонимный чат")
print("тут ты можешь писать кому хочешь и что хочешь!")
print("		 Начнём!")
print("")


#Тут мы вызываем функцию первой регистрации
try:
    file = open("name.txt", "r")
    print("Твой ник:", file.read())
    file.close()
except FileNotFoundError:
    FirstRegistration()

UHaveNewMessage()

#ПРИ НОРМАЛЬНОЙ РАБОТЕ ЭТО СООБЩЕНИЕ НЕ ДОЛЖНО ПОЯВЛЯТСЯ !!!
input("Press 'ENTER' to continue")
