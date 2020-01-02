import re
import sys
import webbrowser

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5 import uic

from datetime import datetime

### 상단바 페이지
import exercise_page
import analysis_page
import board_page
import info_page
import home_page

main_form = uic.loadUiType("./qt_design/main.ui")[0]

class MainWindow(QMainWindow, main_form):
    ### 상단 버튼 start ###
    def btn_help_clicked(self):
        self.dialog = info_page.InfoWindow()
        self.dialog.show()

    def btn_logout_clicked(self):
        QMessageBox.about(self, "pop up", "로그아웃 합니다.!!")
        self.dialog = home_page.HomeWindow()
        self.dialog.show()
        self.close()
    ### 상단 버튼 end ###

    ### 사이드 버튼 start ### 
    def btn_profile_clicked(self):
        file_name = QFileDialog.getOpenFileName(self)[0]
        if not (file_name): QMessageBox.about(self, "pop up", "이미지를 선택해주세요!!"); return 0

        self.lb_user_photo.setPixmap(QtGui.QPixmap(file_name))
        self.photo_path = file_name

    def btn_selectDay_clicked(self):
        today = datetime.today()
        select_day = self.calendarWidget.selectedDate()
        
        if(select_day != None and select_day > today):
            fm = QTextCharFormat() 
            fm.setForeground(Qt.red) 
            fm.setBackground(Qt.yellow)

            self.calendarWidget.setDateTextFormat(select_day, fm)
            select_day = str(select_day).split("PyQt5.QtCore.QDate(")[1]
            select_day = re.sub('[^0-9a-zA-Zㄱ-힗]', '', select_day)
            today = today.strftime("%Y%m%d")
            self.dday = int(select_day) - int(today)
            d_day_text = "D - " + str(self.dday) + " 일"

            self.lb_Dday_num.setText(d_day_text)
        else: QMessageBox.about(self, "pop up", "올바른 목표 날짜를 선택해주세요!!"); return 0
    
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
        self.dialog = analysis_page.AnalysisWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()

    def btn_board_clicked(self):
        self.dialog = board_page.BoardWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()

    def btn_goToHome_clicked(self):
        print("현재 페이지 입니다.")
    ### 상단 메뉴 end ###

    ### 추가 버튼 start ### 
    def btn_movie_1_clicked(self):
        webbrowser.open('https://youtu.be/tV1Dc-LCZJw')
    
    def btn_movie_2_clicked(self):
        webbrowser.open('https://youtu.be/MwC-i3sHnhI')

    def btn_movie_3_clicked(self):
        webbrowser.open('https://youtu.be/bPCriDPI4Oc')
    ### 추가 버튼 end ### 

    def __init__(self, dDay=None, profile_path=None):
        super().__init__()
        self.setupUi(self)
        
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
        self.btn_selectDay.clicked.connect(self.btn_selectDay_clicked)

        self.btn_startExercise.clicked.connect(self.btn_startExercise_clicked)
        self.btn_myData.clicked.connect(self.btn_myData_clicked)
        self.btn_board.clicked.connect(self.btn_board_clicked)
        self.btn_goToHome.clicked.connect(self.btn_goToHome_clicked)
        ### basic button event end ###

        ### 추가 버튼 start ### 
        self.btn_movie_1.clicked.connect(self.btn_movie_1_clicked)
        self.btn_movie_2.clicked.connect(self.btn_movie_2_clicked)
        self.btn_movie_3.clicked.connect(self.btn_movie_3_clicked)
        ### 추가 버튼 end ### 