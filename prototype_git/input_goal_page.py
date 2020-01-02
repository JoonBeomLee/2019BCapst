import re
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

input_goal_form = uic.loadUiType("./qt_design/input_goal.ui")[0]

class InputGoalWindow(QDialog, input_goal_form):
    def btn_ok_clicked(self):
        input_goal = self.txt_goal.text()
        self.goal = input_goal
        self.close()

    def btn_cancle_clicked(self):
        self.close()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.goal = ""

        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancle.clicked.connect(self.btn_cancle_clicked)