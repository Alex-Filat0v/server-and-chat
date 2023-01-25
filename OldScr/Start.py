user_name = input(str("Введите желаемое имя пользователя: "))
sv = open ("name.txt", "x")
sv.write (user_name)
sv.close()

input("Press 'ENTER' to continue")
