FN = input("Введите имя своего друга, для добавления его в список контактов: ")

sv = open ("FL.txt", "w")
sv.write (FN)
sv.close()

input("Press 'ENTER' to continue")
