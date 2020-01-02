import re
import sys

from email.mime.text import MIMEText

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5 import uic

### 상단바 페이지
import exercise_page
import analysis_page
import main_page
import info_page

board_form = uic.loadUiType("./qt_design/board.ui")[0]

class BoardWindow(QMainWindow, board_form):
    ### 상단 버튼 start ###
    def btn_help_clicked(self):
        self.dialog = info_page.InfoWindow()
        self.dialog.show()

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
        self.dialog = analysis_page.AnalysisWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()

    def btn_board_clicked(self):
        print("현재 페이지 입니다.")

    def btn_goToHome_clicked(self):
        self.dialog = main_page.MainWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()
    ### 상단 메뉴 end ###

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

        self.btn_startExercise.clicked.connect(self.btn_startExercise_clicked)
        self.btn_myData.clicked.connect(self.btn_myData_clicked)
        self.btn_board.clicked.connect(self.btn_board_clicked)
        self.btn_goToHome.clicked.connect(self.btn_goToHome_clicked)
        ### basic button event end ###

        ### web engine view
        self.webEngineView.load(QUrl("https://talk.monsterzym.com/training_community"))