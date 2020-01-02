import re
import sys

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5 import uic

email_form = uic.loadUiType("./qt_design/email.ui")[0]

class EmailAuthWindow(QDialog, email_form):
    def btn_auth_clicked(self):
        input_code = self.txt_authCode.text()
        
        print(input_code)
        print(self.initCode)

        if(input_code != self.initCode): QMessageBox.about(self, "pop up", "잘못된 코드 입니다.\n다시 확인해주세요!!")
        else:
            QMessageBox.about(self, "pop up", "Good!!") 
            self.auth = True
            self.close()

    def __init__(self, code):
        super().__init__()
        self.setupUi(self)
        self.initCode = code
        self.auth = False

        self.btn_auth.clicked.connect(self.btn_auth_clicked)