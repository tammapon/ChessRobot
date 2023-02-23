from operator import truediv
import sys
import os
import time
from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox
from PySide6.QtCore import QFile,QTimer
from PySide6.QtGui import QImage,QPixmap,QIcon
from ui_klui06 import Ui_kluiUI
from klui_chessmain import *
from pyseraillucky2 import *
import threading
from Camera_Calibrate import *
from fullchess import *
import cv2 as cv
from detection_test import *

# import klui_chessmain
####.ui2.py #pyside6-uic klui06.ui > ui_klui06.py
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_kluiUI()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(r'C:\Users\klui\Desktop\3_2\module89\return\klui-return\kluiUI\test_klui\image-klui\bK.png'))
        self.ui.label.setPixmap(QPixmap(r"C:\Users\klui\Desktop\3_2\module89\return\klui-return\kluiUI\test_klui\image-klui\robot.png"))
        self.ui.label_6.setPixmap(QPixmap(r"C:\Users\klui\Desktop\3_2\module89\return\klui-return\kluiUI\test_klui\image-klui\keyboard.png"))
        self.ui.label_129.setPixmap(QPixmap(r"C:\Users\klui\Desktop\3_2\module89\return\klui-return\kluiUI\test_klui\image-klui\contact.png"))
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushButton.clicked.connect(self.FullChessGameClick)
        # self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.clicked.connect(self.ManualChessGameClick)
        self.ui.pushButton_3.clicked.connect(self.RobotJogClick)
        self.ui.pushButton_4.clicked.connect(self.RobotMoveClick)
        self.ui.pushButton_6.clicked.connect(self.ContactClick)
        self.ui.pushButton_5.setEnabled(False)
        # self.ui.pushButton_6.setEnabled(False)
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
        self.ui.pushButton_9.clicked.connect(self.endGameClick)
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
        self.robotrunning=False
        self.airunning=False
        self.camrunning=False
        self.ui.pushButton_21.clicked.connect(self.camcalibrateClick)
        self.ui.pushButton_23.clicked.connect(self.CaptureClick)
        self.failed = True
        self.boardcheck = False
        self.ui.pushButton_8.clicked.connect(self.endTurn_full_Click)


    ########################################################################################## UI PART ##################################
    # to page full chess game
    def FullChessGameClick(self):
        if not self.robotrunning and not self.airunning:
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.robotrunning_popup()
    def ManualChessGameClick(self):
        if not self.robotrunning and not self.airunning:
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.robotrunning_popup()
    def RobotJogClick(self):
        if not self.robotrunning and not self.airunning:
            self.ui.stackedWidget.setCurrentIndex(2)
        else:
            self.robotrunning_popup()
    def RobotMoveClick(self):
        if not self.robotrunning and not self.airunning:
            self.ui.stackedWidget.setCurrentIndex(3)
        else:
            self.robotrunning_popup()
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
        if not self.robotrunning and not self.airunning:
            self.startTimer()
            self.get_chess_board_full()
        else:
            self.robotrunning_popup()
    def GameStart2Click(self):
        if not self.robotrunning and not self.airunning:
            self.startTimer()
            self.get_chess_board_manual()
        else:
            self.robotrunning_popup()
    def startJogClick(self):
        if not self.robotrunning and not self.airunning:
            if robotconnect:
                self.ui.label_94.setText("Robot Jogging Press 'O' to cancel")
                self.robotrunning = True
                Thraed_robot = threading.Thread(target=self.robot_jog)
                Thraed_robot.start()
                # self.robot_jog()
            else :
                self.ui.label_94.setText("Robot not connect pls reconnect")
        else:
            self.robotrunning_popup()
    def startJointMoveClick(self):
        if not self.robotrunning and not self.airunning:
            if robotconnect:
                j1 = self.ui.textEdit_3.toPlainText()
                j2 = self.ui.textEdit_4.toPlainText()
                j3 = self.ui.textEdit_5.toPlainText()
                j4 = self.ui.textEdit_6.toPlainText()
                # to_position_joint(int(float(j1)*1000),int(float(j2)*100),int(float(j3)*1000),int(float(j4)*1000))
                # acknowledge()
                self.ui.label_127.setText("Robot Joint Move Running...")
                self.robotrunning = True
                Thraed_robot = threading.Thread(target=self.robotmoveJoint,args=(j1,j2,j3,j4))
                Thraed_robot.start()
        else:
            self.robotrunning_popup()
    def startLinearMoveClick(self):
        if not self.robotrunning and not self.airunning:
            if robotconnect:
                rz = self.ui.textEdit_7.toPlainText()
                x = self.ui.textEdit_9.toPlainText()
                y = self.ui.textEdit_10.toPlainText()
                z = self.ui.textEdit_8.toPlainText()
                # to_position_task(int(float(rz)*1000),int(float(x)*10),int(float(y)*10),int(float(z)*10))
                # acknowledge()
                self.ui.label_127.setText("Robot Linear Move Running...")
                self.robotrunning = True
                Thraed_robot = threading.Thread(target=self.robotmoveTask,args=(rz,x,y,z))
                Thraed_robot.start()
        else:
            self.robotrunning_popup()
    def sethomeClick(self):
        if not self.robotrunning and not self.airunning:
            if robotconnect:
                # sethomeProtocol()
                # acknowledge()
                self.ui.label_127.setText("Robot Home Setting...")
                self.robotrunning = True
                Thraed_robot = threading.Thread(target=self.robotSethome)
                Thraed_robot.start()
        else:
            self.robotrunning_popup()
    def gripperGripClick(self):
        if not self.robotrunning and not self.airunning:
            if gripperconnect:
                self.ui.label_127.setText("Robot Gripper Running...")
                self.robotrunning = True
                self.robotGripper(1)
                self.robotrunning = False
                self.ui.label_127.setText("Normal")
        else:
            self.robotrunning_popup()
    def gripperReleaseClick(self):
        if not self.robotrunning and not self.airunning:
            if gripperconnect:
                self.ui.label_127.setText("Robot Gripper Running...")
                self.robotrunning = True
                self.robotGripper(0)
                self.robotrunning = False
                self.ui.label_127.setText("Normal")
        else:
            self.robotrunning_popup()
    def startChessMoveClick(self):
        if not self.robotrunning and not self.airunning:
            if robotconnect:
                to = self.ui.textEdit_16.toPlainText()
                form = self.ui.textEdit_15.toPlainText()
                form = tfMove(str(form))
                to = tfMove(str(to))
                if self.ui.checkBox_7.isChecked():
                    status = True
                else:
                    status = False
                self.ui.label_127.setText("Robot Chess Move Running...")
                self.robotrunning = True
                Thraed_robot = threading.Thread(target=self.PlayChesstest,args=(form,to,status))
                Thraed_robot.start()
        else:
            self.robotrunning_popup()

    def showTime(self):
        timeDisplay = str(self.min) + ':' + str(self.sec)
        self.ui.label_139.setText(timeDisplay)
        self.ui.label_8.setText(timeDisplay)
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

    def showBoard_full(self):
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][0] + ".png"
        self.ui.a1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][0] + ".png"
        self.ui.a2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][0] + ".png"
        self.ui.a3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][0] + ".png"
        self.ui.a4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][0] + ".png"
        self.ui.a5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][0] + ".png"
        self.ui.a6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][0] + ".png"
        self.ui.a7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][0] + ".png"
        self.ui.a8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][1] + ".png"
        self.ui.b1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][1] + ".png"
        self.ui.b2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][1] + ".png"
        self.ui.b3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][1] + ".png"
        self.ui.b4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][1] + ".png"
        self.ui.b5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][1] + ".png"
        self.ui.b6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][1] + ".png"
        self.ui.b7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][1] + ".png"
        self.ui.b8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][2] + ".png"
        self.ui.c1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][2] + ".png"
        self.ui.c2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][2] + ".png"
        self.ui.c3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][2] + ".png"
        self.ui.c4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][2] + ".png"
        self.ui.c5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][2] + ".png"
        self.ui.c6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][2] + ".png"
        self.ui.c7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][2] + ".png"
        self.ui.c8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][3] + ".png"
        self.ui.d1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][3] + ".png"
        self.ui.d2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][3] + ".png"
        self.ui.d3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][3] + ".png"
        self.ui.d4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][3] + ".png"
        self.ui.d5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][3] + ".png"
        self.ui.d6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][3] + ".png"
        self.ui.d7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][3] + ".png"
        self.ui.d8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][4] + ".png"
        self.ui.e1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][4] + ".png"
        self.ui.e2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][4] + ".png"
        self.ui.e3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][4] + ".png"
        self.ui.e4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][4] + ".png"
        self.ui.e5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][4] + ".png"
        self.ui.e6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][4] + ".png"
        self.ui.e7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][4] + ".png"
        self.ui.e8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][5] + ".png"
        self.ui.f1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][5] + ".png"
        self.ui.f2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][5] + ".png"
        self.ui.f3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][5] + ".png"
        self.ui.f4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][5] + ".png"
        self.ui.f5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][5] + ".png"
        self.ui.f6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][5] + ".png"
        self.ui.f7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][5] + ".png"
        self.ui.f8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][6] + ".png"
        self.ui.g1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][6] + ".png"
        self.ui.g2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][6] + ".png"
        self.ui.g3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][6] + ".png"
        self.ui.g4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][6] + ".png"
        self.ui.g5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][6] + ".png"
        self.ui.g6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][6] + ".png"
        self.ui.g7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][6] + ".png"
        self.ui.g8.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[7][7] + ".png"
        self.ui.h1.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[6][7] + ".png"
        self.ui.h2.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[5][7] + ".png"
        self.ui.h3.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[4][7] + ".png"
        self.ui.h4.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[3][7] + ".png"
        self.ui.h5.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[2][7] + ".png"
        self.ui.h6.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[1][7] + ".png"
        self.ui.h7.setPixmap(QPixmap(img_path))
        img_path= "C:/Users/klui/Desktop/3_2/module89/return/klui-return/kluiUI/test_klui/image-klui/" + self.mainboard[0][7] + ".png"
        self.ui.h8.setPixmap(QPixmap(img_path))
    
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

    def normal_board_full(self):
        self.ui.a1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.a2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.a3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.a4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.a5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.a6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.a7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.a8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.b1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.b2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.b3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.b4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.b5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.b6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.b7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.b8.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.c1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.c2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.c3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.c4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.c5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.c6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.c7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.c8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.d1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.d2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.d3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.d4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.d5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.d6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.d7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.d8.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.e1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.e2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.e3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.e4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.e5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.e6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.e7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.e8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.f1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.f2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.f3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.f4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.f5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.f6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.f7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.f8.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.g1.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.g2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.g3.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.g4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.g5.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.g6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.g7.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.g8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.h1.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.h2.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.h3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.h4.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.h5.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.h6.setStyleSheet(u"background-color: rgb(153, 153, 153);")
        self.ui.h7.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ui.h8.setStyleSheet(u"background-color: rgb(153, 153, 153);")

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
        if not self.robotrunning and not self.airunning:
            self.normal_board()
            self.playerturn()
            self.ui.textEdit.setText('')
            self.ui.textEdit_2.setText('')
        else:
            self.robotrunning_popup()

    def checkClick(self):
        if not self.robotrunning and not self.airunning:
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
        else:
            self.robotrunning_popup()

    def endTurnClick(self):
        if not self.robotrunning and not self.airunning:
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
                self.airunning = True
                Thraed = threading.Thread(target=self.aiturn)
                Thraed.start()
                # self.aiturn()
                print('ai_finshed')
        else:
            self.robotrunning_popup()

    def endGameClick(self):
        if not self.robotrunning and not self.airunning:
            self.ui.checkBox.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
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
            self.showBoard_full()
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
            self.ui.label_9.setText('Turn Status')
            self.ui.label_93.setText("")
            self.endTimer()
            self.min=0
            self.sec=0
            timeDisplay = str(self.min) + ':' + str(self.sec)
            self.ui.label_139.setText(timeDisplay)
            self.ui.label_8.setText(timeDisplay)
        else:
            self.robotrunning_popup()

    def robotrunning_popup(self):
        msg = QMessageBox
        msg.about(self, "warning", "Robot is working... pls wait")
        
    def ContactClick(self):
        if not self.robotrunning and not self.airunning:
            self.ui.stackedWidget.setCurrentIndex(4)
        else:
            self.robotrunning_popup()

    def camcalibrateClick(self):
        if not self.robotrunning and not self.airunning:
            self.robotrunning = True
            port = self.ui.textEdit_11.toPlainText()
            calibrate_cam(int(port))
            self.failed = True
            self.robotrunning = False
        else:
            self.robotrunning_popup()

    def CaptureClick(self):
        if not self.robotrunning and not self.airunning:
            self.robotrunning = True
            port = self.ui.textEdit_11.toPlainText()
            while self.failed:
                self.capture(int(port))
            self.failed = True
            self.firstcheck_board(self.first_detection())
            self.showBoard_full()
            self.robotrunning = False
        else:
            self.robotrunning_popup()

    def endTurn_full_Click(self):
        if not self.robotrunning and not self.airunning:
            if self.humanTurn:
                if self.gs.whiteTomove:
                    self.ui.label_140.setText('Player White Turn')
                else:
                    self.ui.label_140.setText('Player Black Turn')
                self.robotrunning = True
                port = self.ui.textEdit_11.toPlainText()
                camThraed = threading.Thread(target=self.captureloop)
                camThraed.start()
                camThraed.join()
                self.mainboard = chesstrack(self.mainboard,self.color_detection())
                self.showBoard_full()
                self.robotrunning = False
            else:
                if self.gs.whiteTomove:
                    self.ui.label_140.setText('AI White Turn')
                else:
                    self.ui.label_140.setText('AI Black Turn')
                print('AI turn')
                self.airunning = True
                Thraed = threading.Thread(target=self.aiturn)
                Thraed.start()
                # self.aiturn()
                print('ai_finshed')
        else:
            self.robotrunning_popup()

    ########################################################################################## UI PART ##################################

    ###################################################################################### CAMERA PART ###################################

    def captureloop(self):
        while self.failed:
            self.capture(int(port))
        self.failed = True

    def capture(self,port):
        raw = take_picture(port)
        # cv.imshow('frame',test)
        # cv.waitKey(0)
        img = raw

        img_blur=cv.blur(img,(3,3),0)
        gray_blur_kuy = cv.bilateralFilter(img, 9, 75, 75)
        gray_blur_kuy = cv.medianBlur(gray_blur_kuy, 11)

        # cv.imshow('blur', gray_blur_kuy)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        mask=cv.subtract(img,gray_blur_kuy)
        # cv.imshow('mask', mask)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        final=cv.add(img_blur,1*mask)
        # cv.imshow('final', final)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        final = cv.cvtColor(final,cv.COLOR_BGR2GRAY)
        cv.imshow('final2', final)
        cv.waitKey(0)
        cv.destroyAllWindows()

        edges=auto_canny(final)
        cv.imshow('edges', edges)
        cv.waitKey(0)
        cv.destroyAllWindows()

        lines = hough_line(edges)
        # print(lines)
        # print(len(lines))
        lines = reduce_line(lines)
        liness=img.copy()
        show_line(lines,liness)
        cv.imshow('lines', liness)
        cv.waitKey(0)
        cv.destroyAllWindows()

        h_lines, v_lines = h_v_lines(lines)
        points = intersections(h_lines, v_lines )
        points = cluster_points(points)
        print('img shape',img.shape)
        # print(len(points),points,(points[1][0],points[1][1]))
        # img_copy = img
        # for i in range(len(points)) :
        #     cv.circle(img_copy,(int(points[i][0]),int(points[i][1])),5,(255, 0, 0),-1)
        # cv.imshow('points', img_copy)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        # cv.imshow('img', img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        img2=img
        try:
            points=clean_point2(points)
            print('shape point',points.shape)
            # img_copy = img
            # for i in range(len(points)) :
            #     for j in range(len(points)) :
            #         cv.circle(img_copy,(int(points[i][j][0]),int(points[i][j][1])),5,(0, 255, 0),-1)
            # cv.imshow('points2', img_copy)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

            # box=get_box(points,img)
            box=np.zeros(shape=(8,8,4,2),dtype=int)
            # print(box)
            # print(points)
            # print('...........................................................')
            testpoint = np.sort(points,axis=1)
            print('shape testpoint',testpoint.shape)
            # print(testpoint.sort(axis=1))
            # print(points)
            picture=np.float32([[0,0],[124,0],[124,124],[0,124]])
            print('crop picture')
            for i in range(0,8) :
                for j in range(0,8) :
                    box[i][j][0]=testpoint[i][j]
                    box[i][j][1]=testpoint[i][j+1]
                    box[i][j][2]=testpoint[i+1][j+1]
                    box[i][j][3]=testpoint[i+1][j]
                    #########ครอปภาพ
                    my_box=np.float32([box[i][j][0],box[i][j][1],box[i][j][2],box[i][j][3]])
                    my_picture=cv.getPerspectiveTransform(my_box,picture)
                    img_output=cv.warpPerspective(img2,my_picture,(124,124))
                    path = 'kluiUI/klui_tempbox/img'
                    cv.imwrite(os.path.join(path , str(i)+str(j)+'.png'),img_output)
            self.failed = False
        except:
            self.failed = True
        
    def first_detection(self):
        boardchess = get_board_vgg_19_edged()
        # print(boardchess)
        boardchess = predict_encode(boardchess)
        print(boardchess)

        boardcolor = get_board_vgg_19_color()
        # print(boardcolor)
        boardcolor = predict_color(boardcolor)
        print(boardcolor)

        board = combine(boardcolor, boardchess)
        return board

    def color_detection(self):
        boardcolor = get_board_vgg_19_color()
        # print(boardcolor)
        boardcolor = predict_color(boardcolor)
        print(boardcolor)
        return boardcolor

    def firstcheck_board(self,board):
        ssboard = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bp","bp","bp","bp","bp","bp","bp","bp"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["wp","wp","wp","wp","wp","wp","wp","wp"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        if (board == ssboard).all():
            self.mainboard = board
            self.boardcheck = True
        else:
            print('pls try again')

    ###################################################################################### CAMERA PART ###################################

    ########################################################################################## ROBOT MOVE PART ##################################
    def PlayChess(self,now,go,status):
        print('start move')
        # self.robotrunning=True
        print('robotrunnig',self.robotrunning)
        move_chess_2(now,go,status)
        print('end move')
        self.robotrunning=False
        print('robotrunnig',self.robotrunning)
    def PlayChesstest(self,now,go,status):
        print('start move')
        # self.robotrunning=True
        move_chess_2(now,go,status)
        self.robotrunning=False
        self.ui.label_127.setText("Normal")
        print('end move')
    def robot_jog(self):
        print("jogging")
        KeyPressSerial()
        self.robotrunning=False
        self.ui.label_94.setText("Press Start Jog")
    def robotmoveJoint(self,j1,j2,j3,j4):
        to_position_joint(int(float(j1)*1000),int(float(j2)*100),int(float(j3)*1000),int(float(j4)*1000))
        acknowledge()
        self.robotrunning=False
        self.ui.label_127.setText("Normal")
    def robotmoveTask(self,rz,x,y,z):
        to_position_task(int(float(rz)*1000),int(float(x)*10),int(float(y)*10),int(float(z)*10))
        acknowledge()
        self.robotrunning=False
        self.ui.label_127.setText("Normal")
    def robotSethome(self):
        sethomeProtocol()
        acknowledge()
        self.robotrunning=False
        self.ui.label_127.setText("Normal")
    def robotGripper(self,mode):
        GripperProtocol(mode)
        self.robotrunning=False
        self.ui.label_127.setText("Normal")
    ########################################################################################## ROBOT MOVE PART ##################################
    ########################################################################################## CHESS AI PART ##################################

    def get_chess_board_full(self):
        global x_box_now, y_box_now, x_box_go, y_box_go,status
        self.gs = Gamestate(self.mainboard)
        self.validMoves = self.gs.getValidMoves()
        self.moveMade = False # flag variable for when a move is made
        self.running = True
        self.gameOver = False
        if self.ui.checkBox.isChecked():
            self.playerOne = True   # player white if False = AI , True = Player
            self.playerTwo = False   # player black if False = AI , True = Player
            self.ui.label_9.setText('Player White Turn')
        elif self.ui.checkBox_2.isChecked():
            self.playerOne = False   # player white if False = AI , True = Player
            self.playerTwo = True   # player black if False = AI , True = Player
            self.ui.label_9.setText('AI White Turn')
            self.airunning = True
            Thraed = threading.Thread(target=self.aiturn)
            Thraed.start()
        elif self.ui.checkBox_3.isChecked():
            self.playerOne = True   # player white if False = AI , True = Player
            self.playerTwo = True   # player black if False = AI , True = Player
            self.ui.label_9.setText('Player White Turn')
        else:
            pass
        self.showBoard_full()
        print(self.gs.whiteTomove)

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
            self.airunning = True
            Thraed = threading.Thread(target=self.aiturn)
            Thraed.start()
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
                        self.showBoard_full()
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
        # if not self.humanTurn:
        #     if self.gs.whiteTomove:
        #         self.ui.label_140.setText('AI White Turn')
        #     else:
        #         self.ui.label_140.setText('AI Black Turn')
        
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
                self.robotrunning = True
                Thraed_robot = threading.Thread(target=self.PlayChess,args=([x_box_now,y_box_now],[x_box_go,y_box_go],status,))
                Thraed_robot.start()
                # move_chess_2([x_box_now,y_box_now],[x_box_go,y_box_go],status)
            print("finish")
            if AIMove is None:
                AIMove = CheesAI.findRondomMove(self.validMoves)
            self.gs.makeMove(AIMove)
            self.moveMade = True
            # print(gs.board)
            self.showBoard()
            self.showBoard_full()
            Thraed_robot.join()
            # self.robotrunning = False

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
        self.airunning=False

    ########################################################################################## CHESS AI PART ##################################




        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())