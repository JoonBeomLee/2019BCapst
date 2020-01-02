import re
import sys
import pymysql
import smtplib
import hashlib
import pickle

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5 import uic

import email_page
import home_page

sign_form = uic.loadUiType("./qt_design/sign.ui")[0]

with open("./smtp.pkl", "rb") as f:
    data = pickle.load(f)
    smtp_id = data[0]
    smtp_pwd = data[1]

with open("./database_info.pkl", "rb") as f:
    data = pickle.load(f)
    db_host = data[0]
    db_usr = data[1]
    db_pwd = data[2]
    db_name = data[3]

class SignWindow(QMainWindow, sign_form):
    def db_query(self, sql, params, select=False): 
        result = True
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
            result = False
        finally: conn.close()

        return result

    def btn_sign_clicked(self):
        input_id = self.txt_id.text()
        input_name = self.txt_name.text()
        input_pwd = self.txt_pwd.text()
        input_email = self.txt_email.text()

        sql = "insert into playerlist values(%s, %s, md5(%s), %s)"
        params = (input_id, input_name, input_pwd, input_email)
        result = self.db_query(sql, params)

        if(result): QMessageBox.about(self, "pop up", "가입 성공!!")
        else: QMessageBox.about(self, "pop up", "가입 실패!!\n올바르게 입력해주세요!!")

    def btn_home_clicked(self):
        self.dialog = home_page.HomeWindow()
        self.dialog.show()
        self.close()
    
    def btn_id_clicked(self):
        input_id = self.txt_id.text()

        sql = "select count(*) from playerlist where id=%s"
        params = (input_id)
        result = self.db_query(sql, params, True)

        if not(result): 
            QMessageBox.about(self, "pop up", "사용할 수 있는 ID입니다.\nGood!!")
            self.lb_id_status.setEnabled(True)
        else: 
            QMessageBox.about(self, "pop up", "중복된 ID입니다.\n다른 ID를 입력해주세요")
            self.lb_id_status.setEnabled(False)

    def btn_email_clicked(self):
        input_email = self.txt_email.text()

        if not(input_email): QMessageBox.about(self, "pop up", "E-mail을 입력해주세요"); return 0

        init_hashCode = str(hash(input_email))

        smtp = smtplib.SMTP("smtp.naver.com", 587)
        smtp.starttls()  # TLS 사용시 필요
        smtp.login(smtp_id, smtp_pwd)
        msgText = "환영합니다.\n\"Training Manager\" 인증코드 입니다.\n=====  " + init_hashCode + "  =====\n해당 코드로 인증을 해주세요.\n감사합니다!!"
        msg = MIMEText(msgText)
        msg['Subject'] = 'Health Care Certification Code'
        msg['To'] = input_email
        smtp.sendmail(smtp_id, input_email, msg.as_string())
        smtp.quit()

        authForm = email_page.EmailAuthWindow(init_hashCode)
        authForm.exec_()
        print(authForm.auth)

        if(authForm.auth): self.lb_email_status.setEnabled(True)
        else: self.lb_email_status.setEnabled(False)

    def txt_pwd_changed(self):
        label = r'[a-zA-z0-9].*[!,@,#,$,%,^,&,*,?,_,~,-]|[!,@,#,$,%,^,&,*,?,_,~,-].*[a-zA-z0-9]'
        input_pwd = self.txt_pwd.text()

        if re.match(label, input_pwd): self.lb_pwd_status.setEnabled(True); self.lb_pwdStatus.setText("Good!!")
        else: self.lb_pwd_status.setEnabled(False); self.lb_pwdStatus.setText("영문, 숫자, 특수문자를\n포함해주세요.")
        
    def txt_pwdCk_changed(self):
        input_pwd = self.txt_pwd.text()
        input_pwdCk = self.txt_pwdCk.text()

        if(input_pwd == input_pwdCk): self.lb_pwdCk_status.setEnabled(True); self.lb_pwdCKStatus.setText("Good!!")
        else: self.lb_pwdCk_status.setEnabled(False); self.lb_pwdCKStatus.setText("같은 비밀번호를\n입력해주세요!!")

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_home.clicked.connect(self.btn_home_clicked)
        self.btn_sign.clicked.connect(self.btn_sign_clicked)
        self.btn_id.clicked.connect(self.btn_id_clicked)
        self.btn_email.clicked.connect(self.btn_email_clicked)

        self.txt_pwd.textChanged.connect(self.txt_pwd_changed)
        self.txt_pwdCk.textChanged.connect(self.txt_pwdCk_changed)