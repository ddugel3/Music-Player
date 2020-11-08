import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication,QLineEdit,QGroupBox,QProgressBar,QSlider,QProxyStyle,QStyle)

from PyQt5.QtCore import *
from PyQt5 import QtCore,QtGui

class SliderProxyStyle(QProxyStyle):
    def pixelMetric(self, metric, option, widget):
        if metric == QStyle.PM_SliderThickness:
            return 60
        elif metric == QStyle.PM_SliderLength:
            return 40
        return super().pixelMetric(metric, option, widget)
class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.Play()


    def Play(self):
        #button,screen ...
        screen = QGroupBox() #그래프??가 들어갈 공간

        title = QLineEdit('제목이 들어갈 예정') #title
        title.setReadOnly(True)
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)
        title.setMaxLength(50)

        replaybutton = QPushButton() #repeat
        replaybutton.setIcon(QtGui.QIcon('repeat.png'))
        replaybutton.setIconSize(QtCore.QSize(35,35))
        randombutton = QPushButton() #random
        randombutton.setIcon(QtGui.QIcon('shuffle.png'))
        randombutton.setIconSize(QtCore.QSize(35,35))

        self.playbar = QProgressBar(self) #playbar
        self.playbar.setFormat(" ")
        self.playbar.setFont(QtGui.QFont('Arial',22))
        self.playbar.setStyleSheet("QProgressBar::chunk {background-color:rgb(0,0,0)}")


        self.playbutton = QPushButton() #playbutton
        self.playbutton.setIcon(QtGui.QIcon('play.png'))
        self.playbutton.setIconSize(QtCore.QSize(60,60))
        self.playbutton.clicked.connect(self.doAction)
        self.timer = QBasicTimer()
        self.step = 0

        nextbutton = QPushButton()
        nextbutton.setIcon(QtGui.QIcon('next.png'))
        nextbutton.setIconSize(QtCore.QSize(80,60))
        backbutton = QPushButton()
        backbutton.setIcon(QtGui.QIcon('back.png'))
        backbutton.setIconSize(QtCore.QSize(80,60))

        outbutton = QPushButton()
        outbutton.setIcon(QtGui.QIcon('out.png'))
        outbutton.setIconSize(QtCore.QSize(50,50))

        self.volume = QSlider(QtCore.Qt.Vertical)
        style = SliderProxyStyle(self.volume.style())
        self.volume.setStyle(style)
        self.volume.setStyleSheet("QSlider:add-page:vertical{"
                                  "background:rgb(255,0,0)}")
        self.volume.setStyleSheet("QSlider:sub-page:vertical{"
                                  "background:rgb(0,255,0)}")
        self.volume.setStyleSheet("QSlider::handle:vertical{"
                                  "background:rgb(0,0,0)}")

        lyricsbutton = QPushButton()
        lyricsbutton.setIcon(QtGui.QIcon('lyrics.png'))
        lyricsbutton.setIconSize(QtCore.QSize(50,50))

        #layout
        vv1box = QVBoxLayout()
        vv2box = QVBoxLayout()

        vv1_v1box = QVBoxLayout()
        vv1_h0box = QHBoxLayout()
        vv1_h1box = QHBoxLayout()
        vv1_h2box = QHBoxLayout()

        vv1box.addLayout(vv1_v1box)
        vv1_v1box.addWidget(screen)

        vv1box.addLayout(vv1_h0box)
        vv1_h0box.addStretch(1)
        vv1_h0box.addWidget(title)
        vv1_h0box.addStretch(1)

        vv1box.addLayout(vv1_h1box)
        vv1_h1box.addWidget(replaybutton)
        vv1_h1box.addWidget(self.playbar)
        vv1_h1box.addWidget(randombutton)


        vv1box.addLayout(vv1_h2box)
        vv1_h2box.addStretch(1)
        vv1_h2box.addWidget(backbutton)
        vv1_h2box.addWidget(self.playbutton)
        vv1_h2box.addWidget(nextbutton)
        vv1_h2box.addStretch(1)

        vv2_v1box = QVBoxLayout()
        vv2_v2box = QVBoxLayout()
        vv2_v3box = QVBoxLayout()
        vv2_v4box = QVBoxLayout()

        vv2box.addLayout(vv2_v1box)
        vv2_v1box.addWidget(outbutton)

        vv2box.addLayout(vv2_v4box)

        vv2box.addLayout(vv2_v2box)
        vv2_v2box.addWidget(self.volume)

        vv2box.addLayout(vv2_v3box)
        vv2_v3box.addWidget(lyricsbutton)

        mainlayout = QHBoxLayout()
        mainlayout.addLayout(vv1box)
        mainlayout.addLayout(vv2box)

        self.setLayout(mainlayout)

        self.setWindowTitle('main')
        self.setGeometry(500, 200, 1000, 700)
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            return

        self.step = self.step + 1
        self.playbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.playbutton.setIcon(QtGui.QIcon('play.png'))
            self.playbutton.setIconSize(QtCore.QSize(60,60))
        else:
            self.timer.start(100, self)
            self.playbutton.setIcon(QtGui.QIcon('stop.png'))
            self.playbutton.setIconSize(QtCore.QSize(60,60))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    main = Main()
    sys.exit(app.exec_())