import sys
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout,QLabel
from PyQt5.QtCore import QTimer,QDateTime

class WinForm(QWidget):
    def __init__(self,parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('QTimer example')

        self.listFile=QListWidget()
        self.label=QLabel('Label')
        self.startBtn=QPushButton('Start')
        self.endBtn=QPushButton('Stop')

        layout=QGridLayout()

        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)

        layout.addWidget(self.label,0,0,1,2)
        layout.addWidget(self.startBtn,1,0)
        layout.addWidget(self.endBtn,1,1)

        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)

        self.setLayout(layout)

        self.sec=0
        self.min=0

    def showTime(self):
        # time=QDateTime.currentDateTime()
        # timeDisplay=time.toString('yyyy-MM-dd hh:mm:ss dddd')
        timeDisplay = str(self.min) + ':' + str(self.sec)
        self.label.setText(timeDisplay)
        self.sec = self.sec+1
        if self.sec == 60:
            self.min = self.min+1
            self.sec = 0

    def startTimer(self):
        self.timer.start(1000)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=WinForm()
    form.show()
    sys.exit(app.exec_())