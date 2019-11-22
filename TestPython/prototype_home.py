import re
import sys
import pymysql
import smtplib
import hashlib
import pickle

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("./qt_design/mk1_home.ui")[0]
sign_form = uic.loadUiType("./qt_design/mk1_sign.ui")[0]
email_form = uic.loadUiType("./qt_design/mk1_email.ui")[0]

with open("./smtp.pkl", "rb") as f:
    data = pickle.load(f)
    smtp_id = data[0]
    smtp_pwd = data[1]

def db_query(sql, params): 
    # Connect to MySQL 
    conn = pymysql.connect( 
        host='localhost', 
        user='root', 
        password='dblab2316', 
        charset='utf8', db="python_project" 
    )

    try: # create Dictionary Cursor 
        with conn.cursor() as cursor: 
            sql_query = sql 
            cursor.execute(sql_query, params) 
            conn.commit()

            return cursor.fetchall()[0][0]

    except:
        conn.close()

        return False
    finally: 
        conn.close()

class EmailAuthWindow(QDialog, email_form):
    def btn_auth_clicked(self):
        input_code = self.txt_authCode.text()
        
        print(input_code)
        print(self.initCode)

        if(input_code != self.initCode): QMessageBox.about(self, "pop up", "Please input your code!!")
        else:
            QMessageBox.about(self, "pop up", "Success!!") 
            self.auth = True
            self.close()

    def __init__(self, code):
        super().__init__()
        self.setupUi(self)
        self.initCode = code
        self.auth = False

        self.btn_auth.clicked.connect(self.btn_auth_clicked)

class SignWindow(QMainWindow, sign_form):
    def btn_sign_clicked(self):
        input_id = self.txt_id.text()
        input_name = self.txt_name.text()
        input_pwd = self.txt_pwd.text()
        input_pwdCk = self.txt_pwdCk.text()
        input_email = self.txt_email.text()

        sql = "insert into playerlist values(%s, %s, %s, %s);"
        params = (input_id, input_name, input_pwd, input_email)

        if(db_query(sql, params)): QMessageBox.about(self, "pop up", "sign success!!")
        else: QMessageBox.about(self, "pop up", "sign fail!!\nTry again!!")

    def btn_home_clicked(self):
        self.close()

    def btn_id_clicked(self):
        input_id = self.txt_id.text()

        sql = "select count(*) from playerlist where id = %s"
        params = (input_id)
        result = db_query(sql, params)

        print(result, type(result))

        if(db_query(sql, params) == 0): 
            QMessageBox.about(self, "pop up", "Overlap check\nsuccess!!")
            self.lb_id_status.setEnabled(True)

        else: 
            QMessageBox.about(self, "pop up", "Overlap check\nFail!!\nPlease input other ID")
            self.lb_id_status.setEnabled(False)

    def btn_email_clicked(self):
        input_email = self.txt_email.text()
        init_hashCode = str(hash(input_email))

        smtp = smtplib.SMTP("smtp.naver.com", 587)
        smtp.starttls()  # TLS 사용시 필요
        smtp.login(smtp_id, smtp_pwd)
        msgText = "Wellcome\nHealthCare Check this certification Code\n=====  " + init_hashCode + "  =====\nPlease enter this code\nThank You!!"
        msg = MIMEText(msgText)
        msg['Subject'] = 'Health Care Certification Code'
        msg['To'] = input_email
        smtp.sendmail(smtp_id, input_email, msg.as_string())
        smtp.quit()

        authForm = EmailAuthWindow(init_hashCode)
        authForm.exec_()
        print(authForm.auth)

        if(authForm.auth): self.lb_id_status.setEnabled(True)
        else: self.lb_id_status.setEnabled(False)

    def txt_pwd_changed(self):
        input_pwd = self.twt_pwd.text()

        if re.match(r'[A-Za-z0-9@#$]{6,12}', input_pwd):
            self.lb_id_status.setEnabled(True)
        else: 
            self.lb_id_status.setEnabled(False)


    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_home.clicked.connect(self.btn_home_clicked)
        self.btn_sign.clicked.connect(self.btn_sign_clicked)
        self.btn_id.clicked.connect(self.btn_id_clicked)
        self.btn_email.clicked.connect(self.btn_email_clicked)

        self.txt_pwd.textChanged.connect(self.txt_pwd_changed)

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def btn_sign_clicked(self):
        self.dialog = SignWindow()
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