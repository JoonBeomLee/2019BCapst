import re
import sys
import cv2
import threading

from email.mime.text import MIMEText

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5 import uic

### 상단바 페이지
import exercise_page
import main_page
import analysis_page
import board_page
import info_page

train_running = False
model_running = False

ex_ham_in_form = uic.loadUiType("./qt_design/exercise_ham_in.ui")[0]

class ExerciseHamInWindow(QMainWindow, ex_ham_in_form):
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
        self.dialog = board_page.BoardWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()

    def btn_goToHome_clicked(self):
        self.dialog = main_page.MainWindow(self.dday, self.photo_path)
        self.dialog.show()
        self.close()
    ### 상단 메뉴 end ###

    ### 추가 버튼 start ### 
    def train_run(self):
        global train_running

        cam = cv2.VideoCapture("./qt_design/movie/ham.mp4")
        cam.set(3, 240); cam.set(4, 300)

        input_fps = cam.get(cv2.CAP_PROP_FPS)
        ret_val, orig_image = cam.read()

        while train_running:
            cv2.waitKey(10)

            if cam.isOpened() is False or ret_val is False:
                break

            # qt gui에 출력 하기 위한 변환
            orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
            h,w,c = orig_image.shape
            qImg = QtGui.QImage(orig_image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.lb_train.setPixmap(pixmap)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ret_val, orig_image = cam.read()

        cam.release()
        cv2.destroyAllWindows()

    def model_run(self):
        global model_running
        cam = cv2.VideoCapture("./qt_design/movie/video_ham.mp4")
        cam.set(3, 200); cam.set(4, 300)

        input_fps = cam.get(cv2.CAP_PROP_FPS)
        ret_val, orig_image = cam.read()

        while model_running:
            cv2.waitKey(10)

            if cam.isOpened() is False or ret_val is False:
                break

            # qt gui에 출력 하기 위한 변환
            orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
            h,w,c = orig_image.shape
            qImg = QtGui.QImage(orig_image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.lb_model.setPixmap(pixmap)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ret_val, orig_image = cam.read()

        cam.release()
        cv2.destroyAllWindows()

    def count_run(self):
        global count_running

        cam = cv2.VideoCapture("./qt_design/movie/count_ham.MPEG")
        cam.set(3, 110); cam.set(4, 450)

        input_fps = cam.get(cv2.CAP_PROP_FPS)
        ret_val, orig_image = cam.read()

        while count_running:
            cv2.waitKey(10)

            if cam.isOpened() is False or ret_val is False:
                break

            # qt gui에 출력 하기 위한 변환
            orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
            h,w,c = orig_image.shape
            qImg = QtGui.QImage(orig_image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.lb_cnt_box.setPixmap(pixmap)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ret_val, orig_image = cam.read()

        cam.release()
        cv2.destroyAllWindows()

    # 운동 영상 버튼
    def train_stop(self):
        global train_running
        global count_running

        train_running = False
        count_running = False

        train_img = QtGui.QPixmap("./qt_design/img/logo.JPG")
        train_img = train_img.scaled(240, 300, QtCore.Qt.KeepAspectRatio)
        self.lb_train.setPixmap(train_img)

        count_img = QtGui.QPixmap("./qt_design/img/img_three.JPG")
        count_img = count_img.scaled(450, 110, QtCore.Qt.KeepAspectRatio)
        self.lb_cnt_box.setPixmap(count_img)

        print("train stopped")

    def train_start(self):
        global train_running
        global count_running

        train_running = True
        count_running = True

        train_thread = threading.Thread(target=self.train_run)
        train_thread.start()

        count_thread = threading.Thread(target=self.count_run)
        count_thread.start()

        print("train start")

    # 모델 영상 버튼
    def model_start(self):
        global model_running
        model_running = True
        model_thread = threading.Thread(target=self.model_run)
        model_thread.start()
        print("model start")
    
    def model_stop(self):
        global model_running
        model_running = False

        return_img = QtGui.QPixmap("./qt_design/img/ex_ham_model.JPG")
        return_img = return_img.scaled(300, 200, QtCore.Qt.KeepAspectRatio)
        self.lb_model.setPixmap(return_img)
        print("model stopped")

    def btn_train_save_clicked(self):
        QMessageBox.about(self, "pop up", "운동을 저장합니다.")
    ### 추가 버튼 end ### 
    ## 추가 버튼 end ###

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

        ### 추가 버튼 start ### 
        self.btn_train_start.clicked.connect(self.train_start)
        self.btn_train_stop.clicked.connect(self.train_stop)
        self.btn_train_save.clicked.connect(self.btn_train_save_clicked)
        
        # 모범 영상 버튼
        self.btn_model_start.clicked.connect(self.model_start)
        self.btn_model_stop.clicked.connect(self.model_stop)
        ### 추가 버튼 end ### 