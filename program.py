from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
import sys
from setup_db import *

class MessageBox():
    def success_box(self, message) :
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()

    def error_box(self, message) :
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

class Login(QMainWindow) :
    def __init__(self) :
        super().__init__()
        uic.loadUi("ui/Login.ui", self)

        self.email = self.findChild(QLineEdit,"txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")

        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
    
    def hiddenOrShow(self,input:QLineEdit, button:QPushButton) :
        if input.echoMode() == QLineEdit.EchoMode.Password :
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else :
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

    def login(self):
        msg = MessageBox()
        email = self.email.text().strip()
        password = self.password.text()

        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return
        
        if password == "" :
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        
        user = get_user_by_email_and_password(email, password)
        if user is not None :
            msg.success_box("Đăng nhập thành công")
            self.show_home(user["id"])
            return
        
        msg.error_box("Email hoặc mật khẩu không đúng")

    def show_home(self, user_id) :
        self.home = Home(user_id)
        self.home.show()
        self.close()

    def show_register(self) :
        self.register = Register()
        self.register.show()
        self.close()

class Register(QMainWindow) :
    def __init__(self) :
        super().__init__()
        uic.loadUi("ui/Register.ui", self)

        self.name = self.findChild(QLineEdit, "txt_name")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_eye_p = self.findChild(QPushButton,"btn_eye_p")
        self.btn_eye_cp = self.findChild(QPushButton,"btn_eye_cp")

        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
        self.btn_eye_cp.clicked.connect(lambda: self.hiddenOrShow(self.confirm_password, self.btn_eye_cp))
    
    def hiddenOrShow(self,input:QLineEdit, button:QPushButton) :
        if input.echoMode() == QLineEdit.EchoMode.Password :
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else :
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
    
    def register(self) :
        msg = MessageBox()
        name = self.name.text().strip()
        email = self.name.text().strip()
        password = self.password.text().strip()
        confirm_password = self.confirm_password.text().strip()

        if name == "" :
            msg.error_box("Họ tên không được để trống")
            self.name.setFocus()
            return

        if email == "" :
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return
        
        if password == "" :
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        
        if confirm_password == "" :
            msg.error_box("Xác nhận mật khẩu không được để trống")
            self.confirm_password.setFocus()
            return
        
        if password != confirm_password :
            msg.error_box("Mật khẩu không trùng khớp")
            self.confirm_password.setText("")
            self.password.setFocus()
            return
        
        if not self.validate_email(email) :
            msg.error_box("Email không hợp lệ")
            self.email.setFocus()
            return
        
        check_email = get_user_by_email(email)
        if check_email is not None:
            msg.error_box("Email đã tồn tại")
            return
        
        create_user(name, email, password)
        msg.success_box("Đăng ký thành công")
        self.show_login()

    def show_login(self) :
        self.login = Login()
        self.login.show()
        self.close()

    def validate_email(self,s):
            idx_at = s.find('@')
            if idx_at == -1 :
                return False
            return '.' in s[idx_at+1:]
        
class Home(QMainWindow) :
    def __init__(self, user_id) :
        super().__init__()
        uic.loadUi("ui/mainwindow.ui", self)

        self.user_id = user_id
        self.user = get_user_by_id(user_id)
        self.loadAccountInfo()
        
        self.main_widget = self.findChild(QStackedWidget, "main_widget")
        self.btn_nav_home = self.findChild(QPushButton, "btn_nav_home")
        self.btn_nav_play = self.findChild(QPushButton, "btn_nav_play")
        self.btn_watch = self.findChild(QPushButton, "btn_watch")
        self.btn_nav_profile = self.findChild(QPushButton, "btn_nav_profile")
        self.btn_logout = self.findChild(QPushButton, "btn_logout")
        self.btn_radioMale = self.findChild(QRadioButton, "radio_male")
        self.btn_radioFemale = self.findChild(QRadioButton, "radio_female")
        self.btn_avatar = self.findChild(QPushButton,"btn_avatar")
        self.lb_avatar = self.findChild(QLabel,"lb_avatar")
        self.btn_save = self.findChild(QPushButton, "btn_save")
        self.btn_avatar.clicked.connect(self.update_avatar)

        self.main_widget.setCurrentIndex(0)
        self.btn_nav_home.clicked.connect(lambda: self.navMainScreen(0))
        self.btn_nav_play.clicked.connect(lambda: self.navMainScreen(1))
        self.btn_watch.clicked.connect(lambda: self.navMainScreen(2))
        self.btn_nav_profile.clicked.connect(lambda: self.navMainScreen(3))
        self.btn_logout.clicked.connect(self.show_login)
        self.btn_save.clicked.connect(self.save_info)
    


    def navMainScreen(self, index):
        self.main_widget.setCurrentIndex(index)
        
    def loadAccountInfo(self):
        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_telephone = self.findChild(QLineEdit, "txt_telephone")
        self.date_birthday = self.findChild(QDateEdit, "date_birthday")
        self.radio_male = self.findChild(QRadioButton, "radio_male")
        self.radio_female = self.findChild(QRadioButton, "radio_female")
        self.lb_avatar = self.findChild(QLabel, "lb_avatar")

        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_telephone.setText(str(self.user["telephone"]))

        birthday_str = self.user.get("birthday", "")
        birthday = QDate.fromString(birthday_str, "dd-MM-yyyy")
        self.date_birthday.setDate(birthday if birthday.isValid() else QDate.currentDate())

        gender = self.user.get("gender", "").lower()
        self.radio_male.setChecked(gender == "male")
        self.radio_female.setChecked(gender == "female")

        avatar = self.user.get("avatar", "")
        if avatar:
            pixmap = QPixmap(avatar)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(self.lb_avatar.width(), self.lb_avatar.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.lb_avatar.setPixmap(pixmap)

    def show_login(self) :
        self.login = Login()
        self.login.show()
        self.close()    

    def save_info(self):
        name = self.txt_name.text()
        email = self.txt_email.text()
        telephone = self.txt_telephone.text()
        birthday = self.date_birthday.date().toString("dd-MM-yyyy")

        if self.radio_male.isChecked():
            gender = "Male"
        elif self.radio_female.isChecked():
            gender = "Female"
        else:
            gender = "Other"

        self.user["name"] = name
        self.user["gender"] = gender
        self.user["email"] = email
        self.user["telephone"] = telephone
        self.user["birthday"] = birthday
        

        update_user_in_db(self.user_id, name, gender, email, telephone, birthday)
        QMessageBox.information(self, "Cập nhật", "Thông tin người dùng đã được lưu.")
    
    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select Image","","Image Files(*.png *.jpg *.jpeg *.bmp)")
        if file :
            self.user["avatar"] = file
            self.lb_avatar.setPixmap(QPixmap(file))
            update_user_avatar(self.user_id, file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())