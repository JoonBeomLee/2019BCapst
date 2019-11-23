import re
import sys
import pymysql
import smtplib
import hashlib
import pickle

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5 import uic

import prototype_sign as sign_page

form_class = uic.loadUiType("./qt_design/mk1_home.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def btn_sign_clicked(self):
        self.dialog = sign_page.SignWindow()
        self.dialog.show()

        print("sign clicked")
    
    def btn_login_clicked(self):
        print("login clicked")
    
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # button event connect
        self.btn_login.clicked.connect(self.btn_login_clicked)
        self.btn_sign.clicked.connect(self.btn_sign_clicked)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()