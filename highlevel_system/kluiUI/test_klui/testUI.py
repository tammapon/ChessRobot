import sys
import os
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile,QTimer
from PySide6.QtGui import QImage,QPixmap,QIcon
from ui_klui05 import Ui_kluiUI
from klui_chessmain import *
from pyseraillucky2 import *
# import klui_chessmain
####.ui2.py #pyside6-uic klui05.ui > ui_klui05.py
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_kluiUI()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(r'C:\Users\klui\Desktop\3_2\module89\return\klui-return\kluiUI\test_klui\image-klui\bK.png'))
        self.ui.label.setPixmap(QPixmap(r"C:\Users\klui\Desktop\3_2\module89\return\klui-return\kluiUI\test_klui\image-klui\robot.png"))
        self.ui.label_6.setPixmap(QPixmap(r"C:\Users\klui\Desktop\3_2\module89\return\klui-return\kluiUI\test_klui\image-klui\keyboard.png"))
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushButton.clicked.connect(self.FullChessGameClick)
        self.ui.pushButton_2.clicked.connect(self.ManualChessGameClick)
        self.ui.pushButton_3.clicked.connect(self.RobotJogClick)
        self.ui.pushButton_4.clicked.connect(self.RobotMoveClick)
        self.ui.pushButton_7.clicked.connect(self.GameStartClick)
        self.ui.pushButton_10.clicked.connect(self.GameStart2Click)
        self.ui.checkBox.clicked.connect(self.checkBoxOne1)
        self.ui.checkBox_2.clicked.connect(self.checkBoxOne2)
        self.ui.checkBox_3.clicked.connect(self.checkBoxOne3)
        self.ui.checkBox_4.clicked.connect(self.checkBoxOne4)
        self.ui.checkBox_5.clicked.connect(self.checkBoxOne5)
        self.ui.checkBox_6.clicked.connect(self.checkBoxOne6)
        self.mainboard=[["bR","bN","bB","bQ","bK","bB","bN","bR"],
                        ["bp","bp","bp","bp","bp","bp","bp","bp"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["wp","wp","wp","wp","wp","wp","wp","wp"],
                        ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.ui.pushButton_13.clicked.connect(self.MoveClick)
        self.ui.pushButton_11.clicked.connect(self.endTurnClick)
        self.ui.pushButton_12.clicked.connect(self.checkClick)
        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)
        self.sec=0
        self.min=0
        self.ui.pushButton_16.clicked.connect(self.endGameClick)
        if robotconnect:
            self.ui.label_97.setText('connected')
            self.ui.label_97.setStyleSheet(u"color: rgb(46, 255, 0);")
        if gripperconnect:
            self.ui.label_98.setText('connected')
            self.ui.label_98.setStyleSheet(u"color: rgb(46, 255, 0);")
        self.ui.pushButton_14.clicked.connect(self.startJogClick)
        self.ui.pushButton_15.clicked.connect(self.startJointMoveClick)
        self.ui.pushButton_17.clicked.connect(self.startLinearMoveClick)
        self.ui.pushButton_18.clicked.connect(self.sethomeClick)
        self.ui.pushButton_19.clicked.connect(self.gripperGripClick)
        self.ui.pushButton_20.clicked.connect(self.gripperReleaseClick)
        self.ui.pushButton_22.clicked.connect(self.startChessMoveClick)
        
    
    # to page full chess game
    def FullChessGameClick(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def ManualChessGameClick(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def RobotJogClick(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def RobotMoveClick(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    def checkBoxOne1(self):
        if self.ui.checkBox.isChecked():
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
    def checkBoxOne2(self):
        if self.ui.checkBox_2.isChecked():
            self.ui.checkBox.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
    def checkBoxOne3(self):
        if self.ui.checkBox_3.isChecked():
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox.setChecked(False)
    def checkBoxOne4(self):
        if self.ui.checkBox_4.isChecked():
            self.ui.checkBox_5.setChecked(False)
            self.ui.checkBox_6.setChecked(False)
    def checkBoxOne5(self):
        if self.ui.checkBox_5.isChecked():
            self.ui.checkBox_4.setChecked(False)
            self.ui.checkBox_6.setChecked(False)
    def checkBoxOne6(self):
        if self.ui.checkBox_6.isChecked():
            self.ui.checkBox_4.setChecked(False)
            self.ui.checkBox_5.setChecked(False)
    def GameStartClick(self):
        if self.ui.checkBox.isChecked():
            pass
        elif self.ui.checkBox_2.isChecked():
            pass
        elif self.ui.checkBox_3.isChecked():
            pass
    def GameStart2Click(self):
        self.startTimer()
        self.get_chess_board_manual()
    def startJogClick(self):
        if robotconnect:
            KeyPressSerial()
        else :
            self.ui.label_94.setText("Robot not connect pls reconnect")
    def startJointMoveClick(self):
        if robotconnect:
            j1 = self.ui.textEdit_3.toPlainText()
            j2 = self.ui.textEdit_4.toPlainText()
            j3 = self.ui.textEdit_5.toPlainText()
            j4 = self.ui.textEdit_6.toPlainText()
            to_position_joint(int(float(j1)*1000),int(float(j2)*100),int(float(j3)*1000),int(float(j4)*1000))
            acknowledge()
    def startLinearMoveClick(self):
        if robotconnect:
            rz = self.ui.textEdit_7.toPlainText()
            x = self.ui.textEdit_9.toPlainText()
            y = self.ui.textEdit_10.toPlainText()
            z = self.ui.textEdit_8.toPlainText()
            to_position_task(int(float(rz)*1000),int(float(x)*10),int(float(y)*10),int(float(z)*10))
            acknowledge()
    def sethomeClick(self):
        if robotconnect:
            sethomeProtocol()
            acknowledge()
    def gripperGripClick(self):
        if gripperconnect:
            GripperProtocol(int(1))
            # acknowledge()
    def gripperReleaseClick(self):
        if gripperconnect:
            GripperProtocol(int(0))
            # acknowledge()
    def startChessMoveClick(self):
        if robotconnect:
            GripperProtocol(int(0))
            acknowledge()


    def showBoard(self):
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][0] + ".png"
        self.ui.ma1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][0] + ".png"
        self.ui.ma2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][0] + ".png"
        self.ui.ma3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][0] + ".png"
        self.ui.ma4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][0] + ".png"
        self.ui.ma5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][0] + ".png"
        self.ui.ma6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][0] + ".png"
        self.ui.ma7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][0] + ".png"
        self.ui.ma8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][1] + ".png"
        self.ui.mb1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][1] + ".png"
        self.ui.mb2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][1] + ".png"
        self.ui.mb3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][1] + ".png"
        self.ui.mb4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][1] + ".png"
        self.ui.mb5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][1] + ".png"
        self.ui.mb6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][1] + ".png"
        self.ui.mb7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][1] + ".png"
        self.ui.mb8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][2] + ".png"
        self.ui.mc1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][2] + ".png"
        self.ui.mc2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][2] + ".png"
        self.ui.mc3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][2] + ".png"
        self.ui.mc4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][2] + ".png"
        self.ui.mc5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][2] + ".png"
        self.ui.mc6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][2] + ".png"
        self.ui.mc7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][2] + ".png"
        self.ui.mc8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][3] + ".png"
        self.ui.md1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][3] + ".png"
        self.ui.md2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][3] + ".png"
        self.ui.md3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][3] + ".png"
        self.ui.md4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][3] + ".png"
        self.ui.md5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][3] + ".png"
        self.ui.md6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][3] + ".png"
        self.ui.md7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][3] + ".png"
        self.ui.md8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][4] + ".png"
        self.ui.me1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][4] + ".png"
        self.ui.me2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][4] + ".png"
        self.ui.me3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][4] + ".png"
        self.ui.me4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][4] + ".png"
        self.ui.me5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][4] + ".png"
        self.ui.me6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][4] + ".png"
        self.ui.me7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][4] + ".png"
        self.ui.me8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][5] + ".png"
        self.ui.mf1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][5] + ".png"
        self.ui.mf2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][5] + ".png"
        self.ui.mf3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][5] + ".png"
        self.ui.mf4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][5] + ".png"
        self.ui.mf5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][5] + ".png"
        self.ui.mf6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][5] + ".png"
        self.ui.mf7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][5] + ".png"
        self.ui.mf8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][6] + ".png"
        self.ui.mg1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][6] + ".png"
        self.ui.mg2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][6] + ".png"
        self.ui.mg3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][6] + ".png"
        self.ui.mg4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][6] + ".png"
        self.ui.mg5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][6] + ".png"
        self.ui.mg6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][6] + ".png"
        self.ui.mg7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][6] + ".png"
        self.ui.mg8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][7] + ".png"
        self.ui.mh1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][7] + ".png"
        self.ui.mh2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][7] + ".png"
        self.ui.mh3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][7] + ".png"
        self.ui.mh4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][7] + ".png"
        self.ui.mh5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][7] + ".png"
        self.ui.mh6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][7] + ".png"
        self.ui.mh7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][7] + ".png"
        self.ui.mh8.setPixmap(QPixmap(img_path))
    
    def normal_board(self):
        self.ui.ma1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.ma2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.ma3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.ma4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.ma5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.ma6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.ma7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.ma8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mb1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mb2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mb3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mb4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mb5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mb6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mb7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mb8.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mc1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mc2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mc3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mc4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mc5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mc6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mc7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mc8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.md1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.md2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.md3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.md4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.md5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.md6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.md7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.md8.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.me1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.me2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.me3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.me4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.me5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.me6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.me7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.me8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mf1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mf2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mf3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mf4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mf5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mf6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mf7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mf8.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mg1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mg2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mg3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mg4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mg5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mg6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mg7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mg8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mh1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mh2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mh3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mh4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mh5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mh6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.mh7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.mh8.setStyleSheet(u"background-color: rgb(153, 153, 153);")

    def check_board(self,lstvalid):
        for i in lstvalid:
            if i == (0,0):
                self.ui.ma8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (0,1):
                self.ui.mb8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (0,2):
                self.ui.mc8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (0,3):
                self.ui.md8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (0,4):
                self.ui.me8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (0,5):
                self.ui.mf8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (0,6):
                self.ui.mg8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (0,7):
                self.ui.mh8.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,0):
                self.ui.ma7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,1):
                self.ui.mb7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,2):
                self.ui.mc7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,3):
                self.ui.md7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,4):
                self.ui.me7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,5):
                self.ui.mf7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,6):
                self.ui.mg7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (1,7):
                self.ui.mh7.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,0):
                self.ui.ma6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,1):
                self.ui.mb6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,2):
                self.ui.mc6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,3):
                self.ui.md6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,4):
                self.ui.me6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,5):
                self.ui.mf6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,6):
                self.ui.mg6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (2,7):
                self.ui.mh6.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,0):
                self.ui.ma5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,1):
                self.ui.mb5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,2):
                self.ui.mc5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,3):
                self.ui.md5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,4):
                self.ui.me5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,5):
                self.ui.mf5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,6):
                self.ui.mg5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (3,7):
                self.ui.mh5.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,0):
                self.ui.ma4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,1):
                self.ui.mb4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,2):
                self.ui.mc4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,3):
                self.ui.md4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,4):
                self.ui.me4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,5):
                self.ui.mf4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,6):
                self.ui.mg4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (4,7):
                self.ui.mh4.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,0):
                self.ui.ma3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,1):
                self.ui.mb3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,2):
                self.ui.mc3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,3):
                self.ui.md3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,4):
                self.ui.me3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,5):
                self.ui.mf3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,6):
                self.ui.mg3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (5,7):
                self.ui.mh3.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,0):
                self.ui.ma2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,1):
                self.ui.mb2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,2):
                self.ui.mc2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,3):
                self.ui.md2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,4):
                self.ui.me2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,5):
                self.ui.mf2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,6):
                self.ui.mg2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (6,7):
                self.ui.mh2.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,0):
                self.ui.ma1.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,1):
                self.ui.mb1.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,2):
                self.ui.mc1.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,3):
                self.ui.md1.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,4):
                self.ui.me1.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,5):
                self.ui.mf1.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,6):
                self.ui.mg1.setStyleSheet(u"background-color: rgb(30, 230, 200);")
            if i == (7,7):
                self.ui.mh1.setStyleSheet(u"background-color: rgb(30, 230, 200);")

    def MoveClick(self):
        self.normal_board()
        self.playerturn()
        self.ui.textEdit.setText('')
        self.ui.textEdit_2.setText('')

    def checkClick(self):
        self.normal_board()
        form = self.ui.textEdit.toPlainText()
        lstvalid=[]
        try:
            form = tfMove(str(form))
            print(form,form[0],form[1])
            lstvalid.append(form)
            for move in self.validMoves:
                if form[0]==move.startRow and form[1]==move.startCol:
                    print((move.endRow,move.endCol))
                    lstvalid.append((move.endRow,move.endCol))
        except:
            print('input from is wrong')
            for move in self.validMoves:
                print(move.startRow,move.startCol)
                lstvalid.append((move.startRow,move.startCol))
        self.check_board(lstvalid)

    def endTurnClick(self):
        if self.humanTurn:
            if self.gs.whiteTomove:
                self.ui.label_140.setText('Player White Turn')
            else:
                self.ui.label_140.setText('Player Black Turn')
        else:
            if self.gs.whiteTomove:
                self.ui.label_140.setText('AI White Turn')
            else:
                self.ui.label_140.setText('AI Black Turn')
            print('AI turn')
            self.aiturn()
            print('ai_finshed')

        
    def get_chess_board_manual(self):
        global x_box_now, y_box_now, x_box_go, y_box_go,status
        self.gs = Gamestate(self.mainboard)
        self.validMoves = self.gs.getValidMoves()
        self.moveMade = False # flag variable for when a move is made
        self.running = True
        self.gameOver = False
        if self.ui.checkBox_4.isChecked():
            self.playerOne = True   # player white if False = AI , True = Player
            self.playerTwo = False   # player black if False = AI , True = Player
            self.ui.label_140.setText('Player White Turn')
        elif self.ui.checkBox_6.isChecked():
            self.playerOne = False   # player white if False = AI , True = Player
            self.playerTwo = True   # player black if False = AI , True = Player
            self.ui.label_140.setText('AI White Turn')
            self.aiturn()
        elif self.ui.checkBox_5.isChecked():
            self.playerOne = True   # player white if False = AI , True = Player
            self.playerTwo = True   # player black if False = AI , True = Player
            self.ui.label_140.setText('Player White Turn')
        else:
            pass
        self.showBoard()
        print(self.gs.whiteTomove)
        # self.ui.label_140.setText('fuck')
        # print(gs.board)
        # self.humanTurn = (self.gs.whiteTomove and self.playerOne) or (not self.gs.whiteTomove and self.playerTwo)
        # print(len(self.validMoves))
    def playerturn(self):
        self.humanTurn = (self.gs.whiteTomove and self.playerOne) or (not self.gs.whiteTomove and self.playerTwo)
        if not self.gameOver and self.humanTurn:
            form = self.ui.textEdit.toPlainText()
            to = self.ui.textEdit_2.toPlainText()
            print(form,to)
            try:
                form = tfMove(str(form))
                to = tfMove(str(to))
                move = ChessEngine_W.Move(form, to, self.gs.board)
                print("Move_Position" , move.getChessNotation())
                
                for i in range(len(self.validMoves)):
                    if move == self.validMoves[i]:
                        self.gs.makeMove(self.validMoves[i])
                        self.moveMade = True
                        if self.gs.send_castle() == "Castling1":
                            if self.gs.whiteTomove == False:
                                pass
                                # print("Castling W - R")
                        if self.gs.send_castle() == "Castling2":
                            if self.gs.whiteTomove == False:
                                pass
                                # print("Castling W - L")
                        if self.gs.send_castle() == "Castling1":
                            if self.gs.whiteTomove == True:
                                pass
                                # print("Castling B - R")
                        if self.gs.send_castle() == "Castling2":
                            if self.gs.whiteTomove == True:
                                pass
                                # print("Castling B - L")
                        print(self.gs.board)
                        self.showBoard()
                        self.ui.label_93.setText("")
                        break
                    else:
                        self.ui.label_93.setText("can't move pls try again")
                        # print('input is wrong')
            except:
                self.ui.label_93.setText("can't move pls try again")
                print('input is wrong')
        if self.moveMade:
            self.validMoves = self.gs.getValidMoves()
    
            self.moveMade = False

        if self.gs.checkMate:
            self.gameOver = True
            if self.gs.whiteTomove:
                self.ui.label_140.setText('Black wins by checkMate')
                # drawText(screen, 'Black wins by checkMate')
                self.endTimer()
            else:
                self.ui.label_140.setText('White wins by checkMate')
                # drawText(screen, 'White wins by checkMate')
                self.endTimer()
        elif self.gs.staleMate:
            self.gameOver = True
            self.ui.label_140.setText('staleMate')
            # drawText(screen, 'staleMate')
            self.endTimer()
        self.humanTurn = (self.gs.whiteTomove and self.playerOne) or (not self.gs.whiteTomove and self.playerTwo)
        if not self.humanTurn:
            if self.gs.whiteTomove:
                self.ui.label_140.setText('AI White Turn')
            else:
                self.ui.label_140.setText('AI Black Turn')
        
    def aiturn(self):
        self.humanTurn = (self.gs.whiteTomove and self.playerOne) or (not self.gs.whiteTomove and self.playerTwo)
        if not self.gameOver and not self.humanTurn:
            AIMove = CheesAI.findBestMove(self.gs, self.validMoves)
            pos_ai = ChessEngine_W.Move.getChessNotation(AIMove)
            
            # print(find_pos1(pos_ai))
            x_box_now = find_pos1(pos_ai)[1]
            y_box_now = find_pos1(pos_ai)[0]
            x_box_go = find_pos1(pos_ai)[3]
            y_box_go = find_pos1(pos_ai)[2]
            status = is_occuppied(self.gs.board, pos_ai)
            # print("pos_now = ",x_box_now,y_box_now," pos_go = ",x_box_go,y_box_go)
            print("Move_Position =", pos_ai)
            print("status =", status)
            if robotconnect:
                print('kk')
                move_chess_2([x_box_now,y_box_now],[x_box_go,y_box_go],status)
            print("finish")
            if AIMove is None:
                AIMove = CheesAI.findRondomMove(self.validMoves)
            self.gs.makeMove(AIMove)
            self.moveMade = True
            # print(gs.board)
            self.showBoard()


        if self.moveMade:
            self.validMoves = self.gs.getValidMoves()
    
            self.moveMade = False

        if self.gs.checkMate:
            self.gameOver = True
            if self.gs.whiteTomove:
                self.ui.label_140.setText('Black wins by checkMate')
                # drawText(screen, 'Black wins by checkMate')
                self.endTimer()
            else:
                self.ui.label_140.setText('White wins by checkMate')
                # drawText(screen, 'White wins by checkMate')
                self.endTimer()
        elif self.gs.staleMate:
            self.gameOver = True
            self.ui.label_140.setText('staleMate')
            # drawText(screen, 'staleMate')
            self.endTimer()
        self.humanTurn = (self.gs.whiteTomove and self.playerOne) or (not self.gs.whiteTomove and self.playerTwo)
        # print(self.humanTurn)
        if self.humanTurn:
            if self.gs.whiteTomove:
                self.ui.label_140.setText('Player White Turn')
            else:
                self.ui.label_140.setText('Player Black Turn')
        else:
            if self.gs.whiteTomove:
                self.ui.label_140.setText('AI White Turn')
            else:
                self.ui.label_140.setText('AI Black Turn')
    def showTime(self):
        timeDisplay = str(self.min) + ':' + str(self.sec)
        self.ui.label_139.setText(timeDisplay)
        self.sec = self.sec+1
        if self.sec == 60:
            self.min = self.min+1
            self.sec = 0

    def startTimer(self):
        self.timer.start(1000)
        self.sec=0
        self.min=0

    def endTimer(self):
        self.timer.stop()

    def endGameClick(self):
        self.ui.checkBox_4.setChecked(False)
        self.ui.checkBox_5.setChecked(False)
        self.ui.checkBox_6.setChecked(False)
        self.mainboard=[["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"]]
        self.showBoard()
        self.mainboard=[["bR","bN","bB","bQ","bK","bB","bN","bR"],
                        ["bp","bp","bp","bp","bp","bp","bp","bp"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["wp","wp","wp","wp","wp","wp","wp","wp"],
                        ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.ui.textEdit.setText('')
        self.ui.textEdit_2.setText('')
        self.ui.label_140.setText('Turn Status')
        self.ui.label_93.setText("")
        self.endTimer()
        self.min=0
        self.sec=0
        timeDisplay = str(self.min) + ':' + str(self.sec)
        self.ui.label_139.setText(timeDisplay)



        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())