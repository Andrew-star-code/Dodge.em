# Form implementation generated from reading ui file 'Authorization.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(425, 425)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_label = QtWidgets.QLabel(self.centralwidget)
        self.main_label.setGeometry(QtCore.QRect(115, 10, 211, 61))
        font = QtGui.QFont("Bender")
        font.setPointSize(26)
        self.main_label.setFont(font)
        self.main_label.setObjectName("main_label")
        self.label_login = QtWidgets.QLabel(self.centralwidget)
        self.label_login.setGeometry(QtCore.QRect(185, 80, 121, 61))
        font = QtGui.QFont("Bender")
        font.setPointSize(18)
        self.label_login.setFont(font)
        self.label_login.setObjectName("label_login")
        self.label_password = QtWidgets.QLabel(self.centralwidget)
        self.label_password.setGeometry(QtCore.QRect(178, 155, 161, 71))
        font = QtGui.QFont("Bender")
        font.setPointSize(18)
        self.label_password.setFont(font)
        self.label_password.setObjectName("label_password")
        self.pushButtonLogin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonLogin.setGeometry(QtCore.QRect(130, 290, 171, 51))
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.pushButtonRegistration = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRegistration.setGeometry(QtCore.QRect(130, 350, 171, 31))
        self.pushButtonRegistration.setObjectName("pushButtonRegistration")
        self.plainTextEditLog = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEditLog.setGeometry(QtCore.QRect(100, 130, 231, 31))
        self.plainTextEditLog.setObjectName("plainTextEditLog")
        self.plainTextEditLog.setPlaceholderText("Введите от 5 до 15 символов")
        self.plainTextEditPass = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEditPass.setGeometry(QtCore.QRect(100, 210, 231, 31))
        self.plainTextEditPass.setObjectName("plainTextEditPass")
        self.plainTextEditPass.setPlaceholderText("Введите от 5 до 15 символов")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 625, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Вход в игру "))
        self.main_label.setText(_translate("MainWindow", "Авторизация"))
        self.label_login.setText(_translate("MainWindow", "Логин"))
        self.label_password.setText(_translate("MainWindow", "Пароль"))
        self.pushButtonLogin.setText(_translate("MainWindow", "Войти"))
        self.pushButtonRegistration.setText(_translate("MainWindow", "Зарегистрироваться"))