# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_name.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NameWindow(object):
    def setupUi(self, NameWindow):
        NameWindow.setObjectName("NameWindow")
        NameWindow.resize(350, 500)
        self.centralwidget = QtWidgets.QWidget(NameWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(75, 260, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(10, 10, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.backButton.setFont(font)
        self.backButton.setObjectName("backButton")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(50, 210, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(75, 180, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(60, 380, 220, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.confirmButton.setFont(font)
        self.confirmButton.setObjectName("confirmButton")
        self.label_text = QtWidgets.QLabel(self.centralwidget)
        self.label_text.setGeometry(QtCore.QRect(30, 60, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_text.setFont(font)
        self.label_text.setText("")
        self.label_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_text.setObjectName("label_text")
        self.password_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.password_2.setGeometry(QtCore.QRect(50, 290, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password_2.setFont(font)
        self.password_2.setObjectName("password_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(75, 110, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.newName = QtWidgets.QLineEdit(self.centralwidget)
        self.newName.setGeometry(QtCore.QRect(50, 140, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.newName.setFont(font)
        self.newName.setText("")
        self.newName.setObjectName("newName")
        NameWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NameWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 350, 21))
        self.menubar.setObjectName("menubar")
        NameWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NameWindow)
        self.statusbar.setObjectName("statusbar")
        NameWindow.setStatusBar(self.statusbar)

        self.retranslateUi(NameWindow)
        QtCore.QMetaObject.connectSlotsByName(NameWindow)

    def retranslateUi(self, NameWindow):
        _translate = QtCore.QCoreApplication.translate
        NameWindow.setWindowTitle(_translate("NameWindow", "MainWindow"))
        self.label_3.setText(_translate("NameWindow", "?????????????????????? ????????????"))
        self.backButton.setText(_translate("NameWindow", "??????????"))
        self.label_2.setText(_translate("NameWindow", "?????????????? ????????????"))
        self.confirmButton.setText(_translate("NameWindow", "??????????????????????"))
        self.label.setText(_translate("NameWindow", "?????????????? ?????????? ??????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NameWindow = QtWidgets.QMainWindow()
    ui = Ui_NameWindow()
    ui.setupUi(NameWindow)
    NameWindow.show()
    sys.exit(app.exec_())
