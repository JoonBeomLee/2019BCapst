import re
import sys
import pymysql
import smtplib
import hashlib
import pickle

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5 import uic

import prototype_email as email_page

sign_form = uic.loadUiType("./qt_design/mk1_sign.ui")[0]

with open("./smtp.pkl", "rb") as f:
    data = pickle.load(f)
    smtp_id = data[0]
    smtp_pwd = data[1]

class SignWindow(QMainWindow, sign_form):
    def db_query(sql, params, select=False): 
        result = False
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
            if(select): result = cursor.fetchall()[0][0]
            result = True
        except: 
            print("except")
        finally: conn.close()

        return result

    def btn_sign_clicked(self):
        input_id = self.txt_id.text()
        input_name = self.txt_name.text()
        input_pwd = self.txt_pwd.text()
        input_pwdCk = self.txt_pwdCk.text()
        input_email = self.txt_email.text()

        sql = "insert into playerlist values(%s, %s, %s, %s);"
        params = (input_id, input_name, input_pwd, input_email)
        result = self.db_query(sql, params)

        print("input data base's result :: ",result)

        if(result): QMessageBox.about(self, "pop up", "sign success!!")
        else: QMessageBox.about(self, "pop up", "sign fail!!\nTry again!!")

    def btn_home_clicked(self):
        self.close()

    def btn_id_clicked(self):
        input_id = self.txt_id.text()

        sql = "select count(*) from playerlist where id = %s"
        params = (input_id)
        result = self.db_query(sql, params)

        print(result, type(result))

        if(self.db_query(sql, params, True) == 0): 
            QMessageBox.about(self, "pop up", "Overlap check\nsuccess!!")
            self.lb_id_status.setEnabled(True)

        else: 
            QMessageBox.about(self, "pop up", "Overlap check\nFail!!\nPlease input other ID")
            self.lb_id_status.setEnabled(False)

    def btn_email_clicked(self):
        input_email = self.txt_email.text()

        if not(input_email): QMessageBox.about(self, "pop up", "Please input your E-Mail"); return 0

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

        authForm = email_page.EmailAuthWindow(init_hashCode)
        authForm.exec_()
        print(authForm.auth)

        if(authForm.auth): self.lb_email_status.setEnabled(True)
        else: self.lb_email_status.setEnabled(False)

    def txt_pwd_changed(self):
        label = r'[a-zA-z0-9].*[!,@,#,$,%,^,&,*,?,_,~,-]|[!,@,#,$,%,^,&,*,?,_,~,-].*[a-zA-z0-9]'
        input_pwd = self.txt_pwd.text()

        if re.match(label, input_pwd): self.lb_pwd_status.setEnabled(True); self.lb_pwdStatus.setText("Good!!")
        else: self.lb_pwd_status.setEnabled(False); self.lb_pwdStatus.setText("Please enter spells, numbers and special characters.")
        
    def txt_pwdCk_changed(self):
        input_pwd = self.txt_pwd.text()
        input_pwdCk = self.txt_pwdCk.text()

        if(input_pwd == input_pwdCk): self.lb_pwdCk_status.setEnabled(True); self.lb_pwdCKStatus.setText("Success!!")
        else: self.lb_pwdCk_status.setEnabled(False); self.lb_pwdCKStatus.setText("Please input same password")

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_home.clicked.connect(self.btn_home_clicked)
        self.btn_sign.clicked.connect(self.btn_sign_clicked)
        self.btn_id.clicked.connect(self.btn_id_clicked)
        self.btn_email.clicked.connect(self.btn_email_clicked)

        self.txt_pwd.textChanged.connect(self.txt_pwd_changed)
        self.txt_pwdCk.textChanged.connect(self.txt_pwdCk_changed)