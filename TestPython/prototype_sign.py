import sys
import pymysql
from PyQt5.QtWidgets import *
from PyQt5 import uic

sign_form = uic.loadUiType("./qt_design/mk1_sign.ui")[0]

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

        if(db_query(sql, params)): QMessageBox.about(self, "pop up", "Overlap check\nsuccess!!")
        else: QMessageBox.about(self, "pop up", "Overlap check\nFail!!\nPlease input other ID")

    def btn_email_clicked(self):
        self.close()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_home.clicked.connect(self.btn_home_clicked)
        self.btn_sign.clicked.connect(self.btn_sign_clicked)
        self.btn_id.clicked.connect(self.btn_id_clicked)
        self.btn_email.clicked.connect(self.btn_email_clicked)

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = SignWindow() 
    myWindow.show()
    app.exec_()