import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType

FormClass, _ = loadUiType(os.path.join(os.path.dirname(__file__), 'dashboard.ui'))

class Dashboard(QMainWindow, FormClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0) 
        self.home_btn_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.dashborad_btn_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.orders_btn_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        self.exit_btn_2.clicked.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
