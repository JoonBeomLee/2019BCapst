import re
import sys

from email.mime.text import MIMEText
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5 import uic

### 상단바 페이지
import exercise_page
import main_page
import board_page
import analysis_ham_page

analysis_arm_form = uic.loadUiType("./qt_design/analysis_arm.ui")[0]

class AnalysisArmWindow(QMainWindow, analysis_arm_form):
    ### 상단 버튼 start ###
    def btn_help_clicked(self):
        QMessageBox.about(self, "pop up", "Info")

    def btn_logout_clicked(self):
        self.close()
    ### 상단 버튼 end ###

    ### 사이드 버튼 start ### 
    def btn_profile_clicked(self):
        file_name = QFileDialog.getOpenFileName(self)[0]
        print(file_name)

        if not (file_name): QMessageBox.about(self, "pop up", "이미지를 선택해주세요!!"); return 0

        self.lb_user_photo.setPixmap(QtGui.QPixmap(file_name))
        self.photo_path = file_name

    # 기존값 전달 받아 초기화
    def init_dday(self):
        d_day_text = "D - " + str(self.dday) + " 일"
        self.lb_Dday_num.setText(d_day_text)

    def init_photo(self):
        self.lb_user_photo.setPixmap(QtGui.QPixmap(self.photo_path))
    ### 사이드 버튼 end ### 

    ### 상단 메뉴 start ###
    def btn_startExercise_clicked(self):
        self.dialog = exercise_page.ExerciseWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()

    def btn_myData_clicked(self):
        print("현재 페이지입니다.")

    def btn_board_clicked(self):
        self.dialog = board_page.BoardWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()

    def btn_goToHome_clicked(self):
        self.dialog = main_page.MainWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()
    ### 상단 메뉴 end ###

    ### 추가 버튼 start ### 
    def listWidget_clicked(self):
        selected_parts = self.listWidget.currentItem().text()
        today = datetime.today().strftime('%Y-%m-%d')
        
        if(selected_parts == "팔"):
            print("현재 페이지 입니다.")

        if(selected_parts == "허벅지"):
            self.dialog = analysis_ham_page.AnalysisHamWindow(self.dday, self.photo_path)
            self.dialog.show()
            self.close()

    def detail_change(self):
        self.detail = self.list_detail.currentItem().text()

        if(self.detail == "콘센트레이션 컬"):
            self.lb_goal_num.setText("150")
            self.lb_goal_today_txt.setText("120")
            self.progressBar.setValue(120 / 150 * 100)

            if(self.unit == None): self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm02_day.png")); return
            if(self.unit == "일"): self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm02_day.png"))
            if(self.unit == "월"): self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm02_month.png"))
            
        if(self.detail == "원암 트라이셉 익스텐션"):
            self.lb_goal_num.setText("100")
            self.lb_goal_today_txt.setText("50")
            self.progressBar.setValue(50 / 100 * 100)

            if(self.unit == None): self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm01_day.png")); return
            if(self.unit == "일"): self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm01_day.png"))
            if(self.unit == "월"): self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm01_month.png"))

    def unit_change(self):
        self.unit = self.list_unit.currentItem().text()

        if(self.unit == "일"):
            if(self.detail == "콘센트레이션 컬"): 
                self.lb_goal_num.setText("150")
                self.lb_goal_today_txt.setText("120")
                self.progressBar.setValue(120 / 150 * 100)
                self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm02_day.png")); return
            else:
                self.lb_goal_num.setText("100")
                self.lb_goal_today_txt.setText("50")
                self.progressBar.setValue(50 / 100 * 100)
                self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm01_day.png")); return

        else:
            if(self.detail == "콘센트레이션 컬"): 
                self.lb_goal_num.setText("150")
                self.lb_goal_today_txt.setText("120")
                self.progressBar.setValue(120 / 150 * 100)
                self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm02_month.png")); return
            else:
                self.lb_goal_num.setText("100")
                self.lb_goal_today_txt.setText("50")
                self.progressBar.setValue(50 / 100 * 100)
                self.lb_plot.setPixmap(QtGui.QPixmap("./qt_design/img/arm01_month.png")); return
    ### 추가 버튼 end ### 

    def __init__(self, dDay=None, profile_path=None):
        super().__init__()
        self.setupUi(self)
        
        self.detail = None
        self.unit = None

        ### 사이드바 인자 start ###
        self.photo_path = profile_path
        self.dday = dDay

        if(self.dday): self.init_dday()
        if(self.photo_path): self.init_photo()
        ### 사이드바 인자 end ###

        ### basic button event start ###
        self.btn_help.clicked.connect(self.btn_help_clicked)
        self.btn_logout.clicked.connect(self.btn_logout_clicked)
        self.btn_profile_change.clicked.connect(self.btn_profile_clicked)

        self.btn_startExercise.clicked.connect(self.btn_startExercise_clicked)
        self.btn_myData.clicked.connect(self.btn_myData_clicked)
        self.btn_board.clicked.connect(self.btn_board_clicked)
        self.btn_goToHome.clicked.connect(self.btn_goToHome_clicked)
        ### basic button event end ###

        ### 추가 버튼 start ### 
        self.listWidget.itemSelectionChanged.connect(self.listWidget_clicked)
        self.list_detail.itemSelectionChanged.connect(self.detail_change)
        self.list_unit.itemSelectionChanged.connect(self.unit_change)
        # day 출력
        self.lb_today_2.setText(datetime.today().strftime('%Y-%m-%d'))
        self.lb_dDay_2.setText("D - " + str(self.dday) + " 일")
        ### 추가 버튼 end ### 