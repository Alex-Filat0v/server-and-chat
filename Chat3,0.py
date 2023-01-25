import socket
import time
from signal import signal, SIGINT
from threading import Thread
import sys
from PyQt5 import QtWidgets
from StartPage import Ui_MainWindow
from Login import Ui_LoginWindow
from registration import Ui_RegistWindow
from MainWindow import Ui_GlobalMainWindow
from settings import Ui_settingsWindow
from change_name import Ui_NameWindow
from change_password import Ui_PassWindow
from id import Ui_pidWindow
from friend import Ui_FriendsWindow
from online import Ui_onlineWindow
from functools import partial


class StartPage(QtWidgets.QMainWindow):
	def __init__(self):
		super(StartPage, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		receive_thread = Thread()
		receive_thread.start()
		self.ui.loginButton.clicked.connect(self.login)
		self.ui.registreButton.clicked.connect(self.register)

	def login(self):
		log_in()

	def register(self):
		first_registration()


class LoginPage(QtWidgets.QMainWindow):
	def __init__(self):
		super(LoginPage, self).__init__()
		self.ui = Ui_LoginWindow()
		self.ui.setupUi(self)
		self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.log_inButton.clicked.connect(self.log_in_check)
		self.ui.backButton.clicked.connect(self.back_login)

	def log_in_check(self):
		global client_log
		global token
		name = self.ui.name.text()
		password = self.ui.password.text()
		if not name or not password:
			self.ui.label_text.setText('Заполните все строки')
		else:
			client.send("CheckName".encode("utf-8"))
			time.sleep(0.1)
			client.send(name.encode("utf-8"))
			client.send(password.encode("utf-8"))
			data = client.recv(2048)
			data = data.decode("utf-8")
			if data == "U":
				self.ui.label_text.setText('Не верно указан логин или пароль')
			else:
				client_log = name
				token = str(data)
				print(token)
				start_main_window()

	def back_login(self):
		back_button()


class RegistrPage(QtWidgets.QMainWindow):
	def __init__(self):
		super(RegistrPage, self).__init__()
		self.ui = Ui_RegistWindow()
		self.ui.setupUi(self)
		self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.log_inButton.clicked.connect(self.registration_check)
		self.ui.backButton.clicked.connect(self.back_register)

	def registration_check(self):
		global client_log
		name = self.ui.name.text()
		password = self.ui.password.text()
		password_2 = self.ui.password_2.text()
		if not name or not password or not password_2:
			self.ui.label_text.setText('Заполните все строки')
		else:
			client.send("FirstRegistration".encode("utf-8"))
			time.sleep(0.1)
			client.send(name.encode("utf-8"))
			data = client.recv(2048)
			data = data.decode("utf-8")
			if data == "PSS":
				client.send(password.encode("utf-8"))
				client.send(password_2.encode("utf-8"))
				data = client.recv(2048)
				data = data.decode("utf-8")
				if data == "SUCCESS":
					client_log = name
					data = client.recv(2048)
					global token
					token = data.decode("utf-8")
					print(token)
					start_main_window()
				else:
					self.ui.label_text.setText('Пароли не совпадают')
			else:
				self.ui.label_text.setText('Такое имя уже занято')

	def back_register(self):
		back_button()


class GlobalMainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(GlobalMainWindow, self).__init__()
		self.ui = Ui_GlobalMainWindow()
		self.ui.setupUi(self)
		self.ui.ExitButton.clicked.connect(self.exit_button)
		self.ui.settingsButton.clicked.connect(self.settings)
		self.ui.Send.clicked.connect(self.send)
		self.ui.updateButton.clicked.connect(self.update_friends)
		self.ui.add_friendButton.clicked.connect(self.add_friends)
		self.ui.now_onlineButton.clicked.connect(self.show_online_ppl)

	def exit_button(self):
		exit()

	def settings(self):
		global setting
		setting = Settings()
		setting.show()

	def update_friends(self):
		self.ui.label_error.setText("")
		client.send("Update".encode("utf-8"))
		data = client.recv(2048)
		data = data.decode("utf-8")
		count = int(data)
		for i in reversed(range(self.ui.verticalLayout.count())):
			self.ui.verticalLayout.takeAt(i).widget().deleteLater()
		if count > 0:
			friends_buttons = [None for i in range(count)]
			for i in range(count):
				data = client.recv(2048)
				data = data.decode("utf-8")
				friends_buttons[i] = QtWidgets.QPushButton()
				friends_buttons[i].setObjectName(str(i))
				friends_buttons[i].setText(str(data))
				self.ui.verticalLayout.addWidget(friends_buttons[i])
				friends_buttons[i].clicked.connect(partial(self.show_message, friends_buttons[i].text()))
		else:
			self.ui.label_error.setText("У вас никого нет в списке друзей")
		
	def show_message(self, friend):
		self.ui.label_error.setText("")
		global fm
		client.send("ShowMessage".encode("utf-8"))
		fm = friend
		client.send(fm.encode("utf-8"))
		data = client.recv(2048)
		data = data.decode("utf-8")
		count = int(data)
		self.ui.plainTextEdit.clear()
		if count > 0:
			for i in range(count):
				data = client.recv(2048)
				data = data.decode("utf-8")
				self.ui.plainTextEdit.appendPlainText(data)
		else:
			self.ui.label_error.setText("У вас нет сообщений от этого пользователя")

	def send(self):
		self.ui.label_error.setText("")
		global fm
		global client_log
		msg = self.ui.messege.text()
		self.ui.messege.setText("")
		if msg != "" and fm != "":
			client.send("NewMessage".encode("utf-8"))			
			client.send(fm.encode("utf-8"))
			data = client.recv(2048)
			data = data.decode("utf-8")
			if data == "NOT UR FRIEND":
				self.ui.label_error.setText("Этого пользователя нет в вашем списке друзей")
			elif data == "2nd test":
				data = client.recv(2048)
				data = data.decode("utf-8")
				if data == "NOT FRIEND":
					self.ui.label_error.setText('Пока пользователь вас не добавит в свой список друзей, вы не можете писать ему!')
				elif data == "FRIEND":
					client.send(msg.encode('utf-8'))
					self.ui.plainTextEdit.appendPlainText(f"{client_log}: {msg}")
					self.ui.label_error.setText('Ваше сообщение было успешно отправленно!')
		elif fm == "":
			self.ui.label_error.setText('Выберите пользователя которому хотите написать!')

	def add_friends(self):
		global friend_app
		friend_app = Friend()
		friend_app.show()

	def show_online_ppl(self):
		global online_ppl
		online_ppl = OnlinePeople()
		online_ppl.show()


class Settings(QtWidgets.QMainWindow):
	def __init__(self):
		super(Settings, self).__init__()
		self.ui = Ui_settingsWindow()
		self.ui.setupUi(self)
		self.ui.backsettingsButton.clicked.connect(self.back)
		self.ui.nameButton.clicked.connect(self.name)
		self.ui.passwordButton.clicked.connect(self.password)
		self.ui.pidButton.clicked.connect(self.pid)

	def back(self):
		global setting
		setting = Settings()
		setting.close()

	def name(self):
		change_u_name()

	def password(self):
		change_u_password()

	def pid(self):
		my_pid()


class ChangeName(QtWidgets.QMainWindow):
	def __init__(self):
		super(ChangeName, self).__init__()
		self.ui = Ui_NameWindow()
		self.ui.setupUi(self)
		self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.backButton.clicked.connect(self.back)
		self.ui.confirmButton.clicked.connect(self.change_name)

	def back(self):
		back_settings()

	def change_name(self):
		name = self.ui.newName.text()
		password = self.ui.password.text()
		password_2 = self.ui.password_2.text()
		client.send("ChangeUName".encode("utf-8"))
		if not name or not password or not password_2:
			self.ui.label_text.setText('Заполните все строки')
		else:
			time.sleep(0.1)
			client.send(password.encode("utf-8"))
			time.sleep(0.1)
			client.send(password_2.encode("utf-8"))
			if password != password_2:
				self.ui.label_text.setText('Пароли не совпадают')
			else:
				data = client.recv(2048)
				data = data.decode("utf-8")
				if data == "PSS":
					time.sleep(0.1)
					client.send(name.encode('utf-8'))
					data = client.recv(2048)
					data = data.decode("utf-8")
					if data == "NA":
						self.ui.label_text.setText(f"Ник был изменен теперь вы {name}")
						time.sleep(0.1)
						back_settings()
					else:
						self.ui.label_text.setText('Это имя уже занято')
				else:
					self.ui.label_text.setText('Неправильно введен пароль')


class ChangePssword(QtWidgets.QMainWindow):
	def __init__(self):
		super(ChangePssword, self).__init__()
		self.ui = Ui_PassWindow()
		self.ui.setupUi(self)
		self.ui.old_pass.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.old_pass_2.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.newPass.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.backButton.clicked.connect(self.back)
		self.ui.confirmButton.clicked.connect(self.change_password)

	def back(self):
		back_settings()

	def change_password(self):
		global token
		new_pass = self.ui.newPass.text()
		old_pass = self.ui.old_pass.text()
		old_pass_2 = self.ui.old_pass_2.text()
		person_id = self.ui.person_id.text()
		client.send("ChangeUPass".encode('utf-8'))
		time.sleep(0.1)
		client.send(token.encode("utf-8"))
		if not new_pass or not old_pass or not old_pass_2 or not person_id:
			self.ui.label_text.setText('Заполните все строки')
		else:
			client.send(old_pass.encode("utf-8"))
			time.sleep(0.1)
			client.send(old_pass_2.encode("utf-8"))
			if old_pass != old_pass_2:
				self.ui.label_text.setText('Пароли не совпадают')
			else:
				data = client.recv(2048)
				data = data.decode("utf-8")
				if data == "PSS":
					client.send(new_pass.encode('utf-8'))
					time.sleep(0.1)
					data = client.recv(2048)
					data = data.decode("utf-8")
					if data == "NAI":
						self.ui.label_text.setText('Новый пароль совпадает со старым')
					else:
						client.send(person_id.encode('utf-8'))
						data = client.recv(2048)
						data = data.decode("utf-8")
						if data == "KOK":
							self.ui.label_text.setText("Пароль был успешно изменен!")
							time.sleep(0.1)
							back_settings()
						else:
							self.ui.label_text.setText('Не верно введен ID')
				else:
					self.ui.label_text.setText('Неправильный пароль')


class PersonPID(QtWidgets.QMainWindow):
	def __init__(self):
		super(PersonPID, self).__init__()
		self.ui = Ui_pidWindow()
		self.ui.setupUi(self)
		self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
		self.ui.backButton.clicked.connect(self.back)
		self.ui.confirmButton.clicked.connect(self.about_id)

	def back(self):
		back_settings()

	def about_id(self):
		global token
		pass_1 = self.ui.password.text()
		pass_2 = self.ui.password_2.text()
		client.send("MyPid".encode("utf-8"))
		time.sleep(0.1)
		client.send(token.encode('utf-8'))
		if not pass_1 or not pass_2:
			self.ui.label_text.setText('Заполните все строки')
		else:
			if pass_1 != pass_2:
				self.ui.label_text.setText('пароли не совпадают')
				client.send("not".encode("utf-8"))
			else:
				client.send("ok".encode("utf-8"))
				time.sleep(0.1)
				client.send(pass_1.encode('utf-8'))
				data = client.recv(2048)
				data = data.decode("utf-8")
				if data != "none":
					self.ui.label.setText(f"ID:{data}")
				else:
					self.ui.label_text.setText('Не верно введен пароль')


class Friend(QtWidgets.QMainWindow):
	def __init__(self):
		super(Friend, self).__init__()
		self.ui = Ui_FriendsWindow()
		self.ui.setupUi(self)
		self.ui.backButton.clicked.connect(self.back)
		self.ui.confirmButton.clicked.connect(self.add_friend)

	def back(self):
		global friend_app
		friend_app = Friend()
		friend_app.close()

	def add_friend(self):
		global client_log
		new_friend = self.ui.friend_name.text()
		new_friend_id = self.ui.friend_id.text()
		if not new_friend or not new_friend_id:
			self.ui.label_text.setText('Заполните все строки')
		else:
			if new_friend == client_log:
				self.ui.label_text.setText('Вы не можете добавить себя в друзья')
			else:
				client.send("AddUFriend".encode("utf-8"))
				time.sleep(0.001)
				client.send(new_friend.encode('utf-8'))
				time.sleep(0.001)
				client.send(new_friend_id.encode('utf-8'))
				data = client.recv(2048)
				data = data.decode("utf-8")
				if data == "KOK":
					data = client.recv(2048)
					data = data.decode("utf-8")
					if data == "KOK":
						self.ui.label_text.setText(f"Теперь {new_friend} является вашим другом")
					else:
						self.ui.label_text.setText(f"{new_friend} уже является вашим другом")
				else:
					self.ui.label_text.setText("Неверное имя или ID друга")


class OnlinePeople(QtWidgets.QMainWindow):
	def __init__(self):
		super(OnlinePeople, self).__init__()
		self.ui = Ui_onlineWindow()
		self.ui.setupUi(self)
		self.ui.backButton.clicked.connect(self.back)
		self.ui.updateButton.clicked.connect(self.show_all_people)

	def back(self):
		global online_ppl
		online_ppl = OnlinePeople()
		online_ppl.close()

	def show_all_people(self):
		client.send("show_all_people".encode("utf-8"))
		data = client.recv(2048)
		count = data.decode("utf-8")
		count = int(count)
		self.ui.plainTextEdit.clear()
		self.ui.plainTextEdit.appendPlainText("Сейчас онлайн:")
		if count > 0:
			for i in range(count):
				data = client.recv(2048)
				data = data.decode("utf-8")
				self.ui.plainTextEdit.appendPlainText(data)


def clean_exit():
	client.send("exit".encode("utf-8"))
	client.close()
	sys.exit(0)


def handler(signal_recv, frame):
	clean_exit()


def first_registration():
	global application
	application.close()
	application = RegistrPage()
	application.show()


def log_in():
	global application
	application.close()
	application = LoginPage()
	application.show()


def back_button():
	global application
	application.close()
	application = StartPage()
	application.show()


def start_main_window():
	global application
	application.close()
	application = GlobalMainWindow()
	application.show()


def back_settings():
	global setting
	setting.close()
	setting = Settings()
	setting.show()


def change_u_name():
	global setting
	setting.close()
	setting = ChangeName()
	setting.show()


def change_u_password():
	global setting
	setting.close()
	setting = ChangePssword()
	setting.show()


def my_pid():
	global setting
	setting.close()
	setting = PersonPID()
	setting.show()


def exit():
	client.send("logout".encode("utf-8"))
	global application
	global setting
	global friend_app
	global online_ppl
	application.close()
	setting.close()
	friend_app.close()
	online_ppl.close()
	time.sleep(0.1)
	application = StartPage()
	application.show()


if __name__ == "__main__":
	signal(SIGINT, handler)
	global fm
	global client
	global token
	global app
	global application
	global setting
	global friend_app
	global online_ppl
	global client_log
	client_log = ""
	fm = ""
	token = None
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_ip = "localhost"
	client.connect((server_ip, 1245))

	app = QtWidgets.QApplication(sys.argv)
	app.aboutToQuit.connect(clean_exit)
	application = StartPage()
	setting = Settings()
	friend_app = Friend()
	online_ppl = OnlinePeople()
	application.show()

	sys.exit(app.exec())
