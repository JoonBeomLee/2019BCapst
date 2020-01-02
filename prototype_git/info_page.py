from PyQt5.QtWidgets import *
from PyQt5 import uic

info_form = uic.loadUiType("./qt_design/help.ui")[0]

class InfoWindow(QDialog, info_form):
    def btn_ok_clicked(self):
        self.close()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_ok.clicked.connect(self.btn_ok_clicked)