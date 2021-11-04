# -*- coding: utf-8 -*-

import os
import os.path
import requests
from time import sleep
import csv
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import joblib
from time import sleep

import ngram_test
import json_to_csv

from PyQt5.QtCore import *
from PyQt5 import QtTest

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import xgboost as xgb
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import plot_importance

REST_URL = 'http://192.168.0.100:8090/tasks/create/file'
LATEST_REPORT_PATH = '/home/cuckoo/.cuckoo/storage/analyses/latest/reports/report.json'
HEADERS = {"Authorization": "Bearer eJhjD_vJ53F9Gp6wRdJv2Q"}
PWD = '/home/cuckoo/GUI/'


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        self.timer = QTimer(MainWindow) # 타이머

        MainWindow.resize(745, 311)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 70, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_open)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(130, 70, 541, 41))
        self.textBrowser.setObjectName("textBrowser")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 120, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.submit_file)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 150, 531, 91))
        self.label.setObjectName("label")


        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(130, 120, 541, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 745, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Malware Classification"))
        self.pushButton.setText(_translate("MainWindow", "파일 선택"))
        self.pushButton_2.setText(_translate("MainWindow", "탐지"))
        self.label.setText(_translate("MainWindow", ""))

    def add_open(self):
        FileOpen = QFileDialog.getOpenFileName(self.pushButton, 'Open file', './')
        self.textBrowser.setText(FileOpen[0])
  
    def timer_progress(self):
        count = self.progressBar.value()
        count += 1
        self.progressBar.setValue(count)

        # ProgressBar의 값이 최대값 이상 Timer를 중지
        if count >= self.progressBar.maximum():
            # 버튼 활성화
            self.pushButton_2.setEnabled(True)
            self.timer.stop()
    
    def submit_file(self):
        self.pushButton_2.setEnabled(False)
        file_path =  self.textBrowser.toPlainText()
        
        with open(file_path, "rb") as sample: # 해당 파일 분석 보내기 
            files = {"file": (file_path, sample)}
            r = requests.post(REST_URL, headers=HEADERS, files=files, timeout=30) # 타임아웃 - 30초 
        
        self.timer.setInterval(1800)
        self.timer.timeout.connect(self.timer_progress)
        self.timer.start()
        self.sleep(180)
        
        f = open(PWD + 'api_order_test.csv', 'a')
        feature = json_to_csv.FeatureExtraction(LATEST_REPORT_PATH)
        wr = csv.writer(f)
        wr.writerow(feature.get_behavior_api_order)
        f.close()
        ngram_test.do_ngram(PWD+"ngram.csv")
        md = joblib.load(PWD + 'model.joblib')
        test = pd.read_csv(PWD + 'ngram_test.csv')
        rns = md.predict(test) 
        
        if rns[0] == 0 : 
            self.label.setText("It's Normal file")
        else : 
            self.label.setText("It's Malware file")
        
    def sleep(self, n):
        QtTest.QTest.qWait(n*1000)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

