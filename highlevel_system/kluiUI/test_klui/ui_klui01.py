# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'klui01.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import os
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QWidget)
# import test_rc

class Ui_kluiUI(object):
    def setupUi(self, kluiUI):
        if not kluiUI.objectName():
            kluiUI.setObjectName(u"kluiUI")
        kluiUI.resize(1080, 720)
        self.centralwidget = QWidget(kluiUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(180, 0, 900, 720))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 900, 720))
        self.stackedWidget.setStyleSheet(u"background-color: rgb(222, 222, 222);")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(390, 80, 47, 14))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(370, 100, 47, 14))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.label_6 = QLabel(self.page_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(420, 130, 47, 14))
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.label_7 = QLabel(self.page_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(440, 140, 47, 14))
        self.stackedWidget.addWidget(self.page_4)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 100, 141, 181))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(u"image: url(:/newPrefix/robot.png);")
        CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(CURRENT_DIRECTORY, "image-klui\robot.png")
        self.label.setPixmap(QPixmap(filename))
        self.label.setScaledContents(True)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 161, 31))
        self.label_2.setStyleSheet(u"font: 75 15pt \"Courier\";")
        self.label_2.setTextFormat(Qt.RichText)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 50, 161, 31))
        self.label_3.setStyleSheet(u"font: 75 15pt \"Courier\";")
        self.label_3.setTextFormat(Qt.RichText)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(False)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(0, 330, 180, 50))
        self.pushButton.setStyleSheet(u"font: 10pt \"Courier\";\n"
"background-color: rgb(230, 230, 230);")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(0, 380, 180, 50))
        self.pushButton_2.setStyleSheet(u"font: 10pt \"Courier\";")
        kluiUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(kluiUI)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(kluiUI)
    # setupUi

    def retranslateUi(self, kluiUI):
        kluiUI.setWindowTitle(QCoreApplication.translate("kluiUI", u"LnwmoduleUI", None))
        self.label_4.setText(QCoreApplication.translate("kluiUI", u"PAGE 1", None))
        self.label_5.setText(QCoreApplication.translate("kluiUI", u"PAGE 2", None))
        self.label_6.setText(QCoreApplication.translate("kluiUI", u"PAGE 3", None))
        self.label_7.setText(QCoreApplication.translate("kluiUI", u"PAGE 4", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("kluiUI", u"LnwModule 8-9", None))
        self.label_3.setText(QCoreApplication.translate("kluiUI", u"FIBO", None))
        self.pushButton.setText(QCoreApplication.translate("kluiUI", u"Chess Game", None))
        self.pushButton_2.setText(QCoreApplication.translate("kluiUI", u"Jog", None))
    # retranslateUi

