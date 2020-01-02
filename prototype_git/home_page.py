import re
import sys
import pymysql
import smtplib
import pickle

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5 import uic

import sign_page
import main_page

home_class = uic.loadUiType("./qt_design/home.ui")[0]

with open("./database_info.pkl", "rb") as f:
    data = pickle.load(f)
    db_host = data[0]
    db_usr = data[1]
    db_pwd = data[2]
    db_name = data[3]

def db_query(sql, params, select=False): 
    result = False
    # Connect to MySQL 
    conn = pymysql.connect( 
        host=db_host, 
        user=db_usr, 
        password=db_pwd, 
        charset='utf8', db=db_name 
    )

    try: # create Dictionary Cursor 
        with conn.cursor() as cursor: 
            sql_query = sql 
            cursor.execute(sql_query, params) 
            
        conn.commit()
        if(select): result = cursor.fetchall()[0][0]
        
    except: 
        print("except")
    finally: conn.close()

    return result

#화면을 띄우는데 사용되는 Class 선언
class HomeWindow(QMainWindow, home_class):
    def btn_sign_clicked(self):
        self.dialog = sign_page.SignWindow()
        self.dialog.show()
        self.close()
    
    def btn_login_clicked(self):
        input_id = self.txt_ID.text()
        input_pwd = self.txt_PW.text()

        if not(input_id): QMessageBox.about(self, "pop up", "ID 를 입력해 주세요."); return 0
        if not(input_pwd): QMessageBox.about(self, "pop up", "PWD 를 입력해 주세요."); return 0

        sql = "select count(*) from playerlist where id=%s and pwd=md5(%s);"
        params = (input_id, input_pwd)
        result = db_query(sql, params, True)

        if (result): QMessageBox.about(self, "pop up", "로그인에 성공 하였습니다.\nGood!!")
        else: QMessageBox.about(self, "pop up", "로그인에 실패 하였습니다.\nID 와 PWD를 확인해 주세요!!"); return 0

        self.dialog = main_page.MainWindow()
        self.dialog.show()
        self.close()
        
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
    myWindow = HomeWindow() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()