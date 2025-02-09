import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType


FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'dashboard.ui'))

class Dashboard(QMainWindow, FormClass):
    def __init__(self, role):
        super().__init__()
        self.setupUi(self)
        self.role = role

        self.stackedWidget.setCurrentIndex(0) 
        self.home_btn_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.dashboard_btn_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.orders_btn_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        self.logout_btn.clicked.connect(self.logout)

        self.configure_permissions()

    def configure_permissions(self):
        if self.role == "Assistant":
            self.dashboard_btn_2.hide()

    def logout(self):

        self.close() 
        from main import MainApp
        self.login_window = MainApp() 
        self.login_window.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard("Assistant")
    window.show()
    sys.exit(app.exec_())
