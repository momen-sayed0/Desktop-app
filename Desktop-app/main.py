import sys, os, sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

#======== load login.ui file=========#
FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'login.ui'))

#========== create database==========#
def create_users_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

#========== insert default users==========#
def insert_default_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("doc", "doc123", "Doctor"))
    except sqlite3.IntegrityError:
        pass
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("assist", "assist123", "Assistant"))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

#========== verify user==========#
def verify_user(username, password, role):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", 
                   (username, password, role))
    user = cursor.fetchone()
    conn.close()
    return user is not None

#========== create users table and insert default users==========#
create_users_table()
insert_default_users()

#========== load dashboard.py file==========#
from dashboard import Dashboard

#========== MainApp class==========#
class MainApp(QWidget, FormClass):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.Handle_Ui()
        self.Handle_buttons()

    #========== handle ui==========#  
    def Handle_Ui(self):
        self.setWindowTitle("Hospital Management System")
         
        #========== hide password==========#
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        
    #========== handle buttons==========#
    def Handle_buttons(self):
        #========== login button==========#
        self.pushButton_login.clicked.connect(self.login)

    #========== login function==========#
    def login(self):
        #========== get username and password==========#
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()

        #========== get role (Doc OR Assist)==========#
        if self.radioButton_doctor.isChecked():
            role = "Doctor"
        elif self.radioButton_assistant.isChecked():
            role = "Assistant"
        else:
            role = None
        #========== check if username and password are empty==========#
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password")
            return
        #========== verify user==========#
        if verify_user(username, password, role):
            QMessageBox.information(self, "Login Success", f"Welcome Ya {role}😎 !")
            #========== open dashboard==========#
            self.dashboard = Dashboard(role)
            self.dashboard.show()
            self.close()  # close login window
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

        #========== clear inputs==========#
        self.lineEdit_username.clear()
        self.lineEdit_password.clear()
        self.radioButton_doctor.setChecked(True)
        self.lineEdit_username.setFocus()

#========== main function==========#
def main():
    app = QApplication(sys.argv)
    style_file = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(style_file):
        with open(style_file, "r") as file:
            app.setStyleSheet(file.read())
    
    login_window = MainApp()
    login_window.show()
    sys.exit(app.exec_())

#========== run main function==========#
if __name__ == '__main__':
    main()  