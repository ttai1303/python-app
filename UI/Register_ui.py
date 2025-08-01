# Form implementation generated from reading ui file '/Users/pinxun/Documents/MindX/PTA/PTA08/TanTai/python-app/UI/Register.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1218, 701)
        MainWindow.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet("background-image: url(img/background.jpg);\n"
"background-repeat: no-repeat;\n"
"background-position: center;")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(40, 60, 291, 51))
        self.label_7.setStyleSheet("font-family: \'Bebas Neue\', sans-serif;\n"
"    font-size: 60px;\n"
"    font-weight: bold;\n"
"    color: #E50914;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 3px;\n"
"    text-align: center;\n"
"    display: inline-block;\n"
"    text-shadow: \n"
"        0px -3px 0px #b20710, \n"
"        0px -6px 0px #8b060c, \n"
"        0px -9px 0px #660508;\n"
"    \n"
"    /* Tạo hiệu ứng cong */\n"
"    display: inline-block;\n"
"    transform: perspective(200px) rotateX(30deg) scaleY(1.5);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(0, 0, 1221, 701))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("/Users/pinxun/Documents/MindX/PTA/PTA08/TanTai/python-app/UI/../img/background.jpg"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.gridWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridWidget.setGeometry(QtCore.QRect(360, 80, 511, 571))
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(parent=self.gridWidget)
        self.widget.setStyleSheet("background: rgba(0, 0, 0, .5);\n"
"border-radius: 20px;\n"
"")
        self.widget.setObjectName("widget")
        self.btn_login = QtWidgets.QPushButton(parent=self.widget)
        self.btn_login.setGeometry(QtCore.QRect(250, 500, 71, 41))
        self.btn_login.setStyleSheet("background-color : transparent")
        self.btn_login.setObjectName("btn_login")
        self.btn_register = QtWidgets.QPushButton(parent=self.widget)
        self.btn_register.setGeometry(QtCore.QRect(110, 450, 291, 41))
        self.btn_register.setStyleSheet("background-color: #e50000;\n"
"border-radius: 7px;\n"
"padding: 5px;\n"
"")
        self.btn_register.setObjectName("btn_register")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setGeometry(QtCore.QRect(110, 180, 41, 20))
        self.label_2.setStyleSheet("background-color : transparent")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setGeometry(QtCore.QRect(110, 90, 71, 20))
        self.label.setStyleSheet("background-color : transparent")
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(parent=self.widget)
        self.label_5.setGeometry(QtCore.QRect(110, 510, 121, 20))
        self.label_5.setStyleSheet("background-color : transparent")
        self.label_5.setObjectName("label_5")
        self.txt_email = QtWidgets.QLineEdit(parent=self.widget)
        self.txt_email.setGeometry(QtCore.QRect(110, 210, 291, 51))
        self.txt_email.setStyleSheet("border-radius: 7px;\n"
"padding: 5px;")
        self.txt_email.setObjectName("txt_email")
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setGeometry(QtCore.QRect(110, 270, 63, 20))
        self.label_3.setStyleSheet("background-color : transparent")
        self.label_3.setObjectName("label_3")
        self.txt_conf_pwd = QtWidgets.QLineEdit(parent=self.widget)
        self.txt_conf_pwd.setGeometry(QtCore.QRect(110, 390, 291, 51))
        self.txt_conf_pwd.setStyleSheet("border-radius: 7px;\n"
"padding: 5px;")
        self.txt_conf_pwd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_conf_pwd.setObjectName("txt_conf_pwd")
        self.txt_password = QtWidgets.QLineEdit(parent=self.widget)
        self.txt_password.setGeometry(QtCore.QRect(110, 300, 291, 51))
        self.txt_password.setStyleSheet("border-radius: 7px;\n"
"padding: 5px;")
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_password.setObjectName("txt_password")
        self.label_4 = QtWidgets.QLabel(parent=self.widget)
        self.label_4.setGeometry(QtCore.QRect(110, 360, 121, 20))
        self.label_4.setStyleSheet("background-color : transparent")
        self.label_4.setObjectName("label_4")
        self.txt_name = QtWidgets.QLineEdit(parent=self.widget)
        self.txt_name.setGeometry(QtCore.QRect(110, 120, 291, 51))
        self.txt_name.setStyleSheet("border-radius: 7px;\n"
"padding: 5px;")
        self.txt_name.setObjectName("txt_name")
        self.label_6 = QtWidgets.QLabel(parent=self.widget)
        self.label_6.setGeometry(QtCore.QRect(110, 10, 151, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color : transparent")
        self.label_6.setObjectName("label_6")
        self.btn_eye_p = QtWidgets.QPushButton(parent=self.widget)
        self.btn_eye_p.setGeometry(QtCore.QRect(360, 310, 41, 29))
        self.btn_eye_p.setStyleSheet("background-image: url(img/eye-slash.svg);\n"
"background-repeat: no-repeat;\n"
"background-position: center;")
        self.btn_eye_p.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/Users/pinxun/Documents/MindX/PTA/PTA08/TanTai/python-app/UI/../img/eye-slash-solid.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_eye_p.setIcon(icon)
        self.btn_eye_p.setObjectName("btn_eye_p")
        self.btn_eye_cp = QtWidgets.QPushButton(parent=self.widget)
        self.btn_eye_cp.setGeometry(QtCore.QRect(360, 400, 41, 29))
        self.btn_eye_cp.setText("")
        self.btn_eye_cp.setIcon(icon)
        self.btn_eye_cp.setObjectName("btn_eye_cp")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.label_8.raise_()
        self.label_7.raise_()
        self.gridWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_7.setText(_translate("MainWindow", "NETFLIX"))
        self.btn_login.setText(_translate("MainWindow", "Log in"))
        self.btn_register.setText(_translate("MainWindow", "Create"))
        self.label_2.setText(_translate("MainWindow", "Email"))
        self.label.setText(_translate("MainWindow", "Username"))
        self.label_5.setText(_translate("MainWindow", "Have an account?"))
        self.txt_email.setPlaceholderText(_translate("MainWindow", "Email"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.txt_conf_pwd.setPlaceholderText(_translate("MainWindow", "Confirm password"))
        self.txt_password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.label_4.setText(_translate("MainWindow", "Confirm password"))
        self.txt_name.setPlaceholderText(_translate("MainWindow", "Username"))
        self.label_6.setText(_translate("MainWindow", "Sign up"))
