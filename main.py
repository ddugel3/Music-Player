import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent

#from home_11 import *


#volume에서 handle 크기 조정
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
        self.showplaylist = QDialog()
        self.currentidx = 0
        self.playlist = QMediaPlaylist()
        self.list = ['../AD-Project/music/stay.wav','../AD-Project/music/잠이 오질 않네요.wav',
                     '../AD-Project/music/Piano-melody_2.mp3','../AD-Project/music/STAY.wav',
                     '../AD-Project/music/Piano-melody_1.wav']
        self.a = QUrl.fromLocalFile('../AD-Project/music/stay-PostMalon.wav')
        self.b = QUrl.fromLocalFile('../AD-Project/music/잠이 오질 않네요-장범준.wav')
        self.c = QUrl.fromLocalFile('../AD-Project/music/Piano-melody_2.mp3')
        self.d = QUrl.fromLocalFile('../AD-Project/music/STAY-BLACKPINK.wav')
        self.e = QUrl.fromLocalFile('../AD-Project/music/Piano-melody_1.wav')
        self.playlist.addMedia(QMediaContent(self.a))
        self.playlist.addMedia(QMediaContent(self.b))
        self.playlist.addMedia(QMediaContent(self.c))
        self.playlist.addMedia(QMediaContent(self.d))
        self.playlist.addMedia(QMediaContent(self.e))
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.Play()

    def Play(self):
        #button,screen ...
        self.screen = QGroupBox()
        self.screen.setStyleSheet("background:rgb(255,255,255)")
        eq = QLabel("Equalizer",self)
        eq.move(25,10)
        eq.resize(100,50)
        self.label = QLabel(self.screen)
        self.label.move(120, 30)
        self.label.resize(800, 400)
        self.movie = QtGui.QMovie("../AD-Project/icon/loading2.gif")
        self.label.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.movie.start()

        self.title = QLineEdit('') #title
        self.title.setReadOnly(True)
        self.title.setMaxLength(1000)
        self.title.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Bold))

        #playbar
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)



        # repeat button
        self.replaybutton = QPushButton()
        self.replaybutton.setIcon(QtGui.QIcon('../AD-Project/icon/repeatone.png'))
        self.replaybutton.setIconSize(QtCore.QSize(35,35))
        self.replaybutton.clicked.connect(self.currretloop)

        # random button
        self.randombutton = QPushButton()
        self.randombutton.setIcon(QtGui.QIcon('../AD-Project/icon/repeat.png'))
        self.randombutton.setIconSize(QtCore.QSize(35,35))
        self.randombutton.clicked.connect(self.loop)

        #playbutton
        self.playbutton = QPushButton()
        self.playbutton.setIcon(QtGui.QIcon('../AD-Project/icon/play.png'))
        self.playbutton.setIconSize(QtCore.QSize(60,60))
        self.playbutton.clicked.connect(self.playClicked)


        #self.playbutton.clicked.connect(self.doAction) #playbutton클릭에 따른 signal
        self.timer = QBasicTimer()
        self.step = 0



        #next button
        self.nextbutton = QPushButton()
        self.nextbutton.setIcon(QtGui.QIcon('../AD-Project/icon/next.png'))
        self.nextbutton.setIconSize(QtCore.QSize(80,60))
        self.nextbutton.clicked.connect(self.nextClicked)


        #back button
        self.backbutton = QPushButton()
        self.backbutton.setIcon(QtGui.QIcon('../AD-Project/icon/back.png'))
        self.backbutton.setIconSize(QtCore.QSize(80,60))
        self.backbutton.clicked.connect(self.prevClicked)


        #out button
        outbutton = QPushButton()
        outbutton.setIcon(QtGui.QIcon('../AD-Project/icon/out.png'))
        outbutton.setIconSize(QtCore.QSize(50,50))
        outbutton.clicked.connect(self.Out)

        # volume
        self.volume = QSlider(QtCore.Qt.Vertical)
        style = SliderProxyStyle(self.volume.style())
        self.volume.setStyle(style)
        self.volume.setStyleSheet("QSlider::handle:vertical{" 
                                  "background:rgb(0,0,0)}")
        self.volume.setRange(0, 100)
        self.volume.setValue(50)
        self.volume.valueChanged[int].connect(self.volumeChanged)

        # lyricsbutton
        self.lyricsbutton = QPushButton()
        self.lyricsbutton.setIcon(QtGui.QIcon('../AD-Project/icon/lyrics.png'))
        self.lyricsbutton.setIconSize(QtCore.QSize(50,50))
        self.lyricsbutton.clicked.connect(self.ShowPLayList)

        #layout
        vv1box = QVBoxLayout()
        vv2box = QVBoxLayout()

        vv1_v1box = QVBoxLayout()
        vv1_h1box = QHBoxLayout()
        vv1_h2box = QHBoxLayout()
        vv1_h3box = QHBoxLayout()


        #screen 띄우는 위치
        vv1box.addLayout(vv1_v1box)
        vv1_v1box.addWidget(self.screen)

        #곡제목 위치
        vv1box.addLayout(vv1_h1box)
        vv1_h1box.addWidget(self.replaybutton)
        vv1_h1box.addWidget(self.title)
        vv1_h1box.addWidget(self.randombutton)

        #replay, playbar, random 버튼 위치
        vv1box.addLayout(vv1_h2box)

        vv1_h2box.addWidget(self.positionSlider)



        #back,play,next 버튼
        vv1box.addLayout(vv1_h3box)
        vv1_h3box.addStretch(1)
        vv1_h3box.addWidget(self.backbutton)
        vv1_h3box.addWidget(self.playbutton)
        vv1_h3box.addWidget(self.nextbutton)
        vv1_h3box.addStretch(1)

        #out, volume, lyrics 버튼
        vv2box.addWidget(outbutton)
        vv2box.addWidget(self.volume)
        vv2box.addWidget(self.lyricsbutton)

        Mainlayout = QHBoxLayout()
        Mainlayout.addLayout(vv1box)
        Mainlayout.addLayout(vv2box)

        self.setLayout(Mainlayout)

        self.setWindowTitle('main')
        self.setGeometry(500, 200, 1000, 700)
        self.show()


    def Out(self):
        self.close()


    def TTitle(self,idx):
        Str = str(self.list[idx]).split("/")
        Str1 = Str[len(Str) - 1].split('.')
        self.title.setText('{}'.format(Str1[0]))


    def playClicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.playbutton.setIcon(QtGui.QIcon('../AD-Project/icon/play.png'))
            self.playbutton.setIconSize(QtCore.QSize(60, 60))
        else:
            self.player.play()
            self.playbutton.setIcon(QtGui.QIcon('../AD-Project/icon/stop.png'))
            self.playbutton.setIconSize(QtCore.QSize(60, 60))
            self.TTitle(self.currentidx)

    def nextClicked(self):
        self.step = 0
        self.currentidx +=1
        self.TTitle(self.currentidx)
        self.playlist.next()


    def prevClicked(self):
        self.step = 0
        self.currentidx -= 1
        self.TTitle(self.currentidx)
        self.playlist.previous()

    def volumeChanged(self):
        self.player.setVolume(self.volume.value())






    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.player.setPosition(position)




    def ShowPLayList(self):


        List = ['stay-PostMalon', '잠이 오질 않네요-장범준','Piano-melody_2', 'STAY-BLACKPINK','Piano-melody_1']

        for (i,j) in zip (List,range(10,110,20)):
            a = QLabel(i, self.showplaylist)
            a.move(10, j)

        label = QLabel(self.showplaylist)
        label.move(0, 110)
        label.resize(100, 100)



        self.showplaylist.setWindowTitle('PlayLIst')
        self.showplaylist.setWindowModality(Qt.ApplicationModal)
        self.showplaylist.setGeometry(1500, 400, 300, 200)
        self.showplaylist.show()


    def closed(self,state):
        self.label.setVisible(state != Qt.Unchecked)


    def currretloop(self):
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

    def loop(self):
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    main = Main()
    sys.exit(app.exec_())