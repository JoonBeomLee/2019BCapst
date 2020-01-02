import re
import sys
import threading
import numpy as np

from email.mime.text import MIMEText
from multiprocessing import Process, Queue

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

### 상단바 페이지
import main_page
import exercise_page
import analysis_page
import board_page
import info_page

##### motion estimation
import os
import argparse
import cv2
import time
import tensorflow

from keras.models import load_model

# home path
# sys.path.append((os.path.dirname("C://Users//DB_LAB//Desktop//19capstone//2019BCapst//prototype//motion_estmation//")))
# lab path
sys.path.append((os.path.dirname("C://Users//joonb//Desktop//prototype//motion_estmation//")))
sys.path.append((os.path.dirname("C:/Users/joonb/Desktop/prototype/motion_estmation/")))
from config_reader import config_reader
from preprocessing import extract_parts, draw
from cmu_model import get_testing_model

# home path
# keras_weights_file = "C://Users//DB_LAB//Desktop//19capstone//2019BCapst//prototype//motion_estmation//ref_data//model.h5"
# lab path
keras_weights_file = "C://Users//joonb//Desktop//prototype//motion_estmation//ref_data//model.h5"
frame_rate_ratio = 2
process_speed = 1

model = get_testing_model()
model.load_weights(keras_weights_file)

# trained_model
train_model = load_model("./motion_estmation/ref_data/arm01_image_classification.h5")

# load config
params, model_params = config_reader()
scale_search = [0.22, 0.25, .5, 1, 1.5, 2]
scale_search = scale_search[0:process_speed]
params['scale_search'] = scale_search

# cam option
width = 240
height = 300
factor = 0.3
resize_fac = 8

train_running = False
model_running = False
count_running = False

ex_arm_in_form = uic.loadUiType("./qt_design/exercise_arm_in.ui")[0]

# 이미지 사이즈 줄이는 함수 // 전체를 가지고 하면 속도가 느려지기 때문에
def crop(image, w, f): 
    return image[:, int(w * f): int(w * (1 - f))]

class ExerciseArmInWindow(QMainWindow, ex_arm_in_form):
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

        cam = cv2.VideoCapture("./motion_estmation/ref_data/train_arm_01.mp4")
        cam.set(3, width); cam.set(4, height) # 3 : width || 4 : height

        input_fps = cam.get(cv2.CAP_PROP_FPS)
        ret_val, orig_image = cam.read()

        # set frame count
        i = 0  # default is 0
        while train_running:
            cv2.waitKey(10)

            if cam.isOpened() is False or ret_val is False:
                break
            
            tic = time.time()

            # skeleton
            cropped = crop(orig_image, width, factor)
            input_image = cv2.resize(cropped, (0, 0), fx=1/resize_fac, fy=1/resize_fac, interpolation=cv2.INTER_CUBIC)        
            input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
            all_peaks, subset, candidate = extract_parts(cropped, params, model, model_params)
            canvas = draw(orig_image, all_peaks, subset, candidate, resize_fac=resize_fac)

            # add remove background only skeleton
            numpy_tmp = np.zeros((canvas.shape[0], canvas.shape[1], 3), dtype=np.uint8)
            canvas_skeleton_gray = draw(numpy_tmp, all_peaks, subset, candidate)
            canvas_skeleton_gray = cv2.cvtColor(canvas_skeleton_gray, cv2.COLOR_BGR2GRAY)

            # judge frame
            chechk_tmp = canvas_skeleton_gray.reshape(1, canvas.shape[0], canvas.shape[1], 1)
            labels = train_model.predict(chechk_tmp)
            
            if(labels[:1][0][0] < labels[1][0][1]):
                # false
            else:
                # true
                print("true")

            # qt gui에 출력 하기 위한 변환
            orig_image = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
            h,w,c = orig_image.shape
            qImg = QtGui.QImage(orig_image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.lb_train.setPixmap(pixmap)

            # print frame 
            #print('Processing frame: ', i)
            toc = time.time()
            #print('processing time is %.5f' % (toc - tic))
            i += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ret_val, orig_image = cam.read()

        cam.release()
        cv2.destroyAllWindows()

    def model_run(self):
        global model_running
        cam = cv2.VideoCapture("./qt_design/movie/video_arm.mp4")
        cam.set(3, 240); cam.set(4, 300)

        input_fps = cam.get(cv2.CAP_PROP_FPS)
        ret_val, orig_image = cam.read()

        while model_running:
            cv2.waitKey(10)

            if cam.isOpened() is False or ret_val is False:
                break
            
            # set tic
            tic = time.time()
   
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

        cam = cv2.VideoCapture("./qt_design/movie/count_arm.MPEG")
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

        count_img = QtGui.QPixmap("./qt_design/img/img_nine.JPG")
        count_img = count_img.scaled(451, 111, QtCore.Qt.KeepAspectRatio)
        self.lb_cnt_box.setPixmap(count_img)

        print("train stopped")

    def train_start(self):
        global train_running
        global count_running

        train_running = True
        count_running = True

        #train_thread = threading.Thread(target=self.train_run)
        #train_thread.start()

        self.train_run()
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

        return_img = QtGui.QPixmap("./qt_design/img/ex_arm_model.JPG")
        return_img = return_img.scaled(300, 200, QtCore.Qt.KeepAspectRatio)
        self.lb_model.setPixmap(return_img)
        print("model stopped")

    def btn_train_save_clicked(self):
        QMessageBox.about(self, "pop up", "운동을 저장합니다.")
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

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    #WindowClass의 인스턴스 생성
    myWindow = ExerciseArmInWindow() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()