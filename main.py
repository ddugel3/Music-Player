import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore,QtGui
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from home_11 import *

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
        screen = QGroupBox() #그래프??가 들어갈 공간

        self.title = QLineEdit('') #title
        self.title.setReadOnly(True)
        self.title.setMaxLength(1000)
        self.title.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))



        # repeat button
        replaybutton = QPushButton()
        replaybutton.setIcon(QtGui.QIcon('../AD-Project/icon/repeat.png'))
        replaybutton.setIconSize(QtCore.QSize(35,35))

        # random button
        randombutton = QPushButton()
        randombutton.setIcon(QtGui.QIcon('../AD-Project/icon/shuffle.png'))
        randombutton.setIconSize(QtCore.QSize(35,35))

        # playbar 재생정
        self.playbar = QProgressBar(self)
        self.playbar.setFormat(" ")
        self.playbar.setFont(QtGui.QFont('Arial',22))
        self.playbar.setStyleSheet("QProgressBar::chunk {background-color:rgb(0,0,0)}")

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
        vv1_v1box.addWidget(screen)

        #곡제목 위치
        vv1box.addLayout(vv1_h1box)
        vv1_h1box.addStretch(1)
        vv1_h1box.addWidget(self.title)
        vv1_h1box.addStretch(1)

        #replay, playbar, random 버튼 위치
        vv1box.addLayout(vv1_h2box)
        vv1_h2box.addWidget(replaybutton)
        vv1_h2box.addWidget(self.playbar)
        vv1_h2box.addWidget(randombutton)

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
        """self.files = QFileDialog.getOpenFileNames(self, 'Select one or more files to open', '','Sound (*.mp3 *.wav *.ogg *.flac *.wma)')
        self.f = self.files[0]
        Str = str(self.f[0]).split("/")
        Str1 = Str[len(Str) - 1].split('.')
        self.title.setText('{}'.format(Str1[0]))
        self.playlist = QMediaPlaylist()
        elf.url = QUrl.fromLocalFile('../AD-Project/music/Piano-melody_2.mp3')
        self.a = QUrl.fromLocalFile('../AD-Project/music/STAY - BLACKPINK.wav')
        self.playlist.addMedia(QMediaContent(self.url))
        self.playlist.addMedia(QMediaContent(self.a))
        self.list = QMediaPlaylist()
        for i in range(0,len(f)):
            self.list.append(f[i])
            print(self.list)
        for path in lists:
            url2 = QUrl.fromLocalFile(path)
            self.list.addMedia(QMediaContent(url2))
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)"""

    def TTitle(self,idx):
        Str = str(self.list[idx]).split("/")
        Str1 = Str[len(Str) - 1].split('.')
        self.title.setText('{}'.format(Str1[0]))


    def playClicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.timer.stop()
            self.playbutton.setIcon(QtGui.QIcon('../AD-Project/icon/play.png'))
            self.playbutton.setIconSize(QtCore.QSize(60, 60))
        else:
            self.player.play()
            self.timer.start(100,self)
            self.playbutton.setIcon(QtGui.QIcon('../AD-Project/icon/stop.png'))
            self.playbutton.setIconSize(QtCore.QSize(60, 60))
            self.TTitle(self.currentidx)

    def nextClicked(self):
        self.step = 0
        self.currentidx +=1
        self.TTitle(self.currentidx)
        if self.player.state() == QMediaPlayer.PlayingState:
            self.timer.start(100, self)
        self.playlist.next()

    def prevClicked(self):
        self.step = 0
        self.currentidx -= 1
        self.TTitle(self.currentidx)
        if self.player.state() == QMediaPlayer.PlayingState:
            self.timer.start(100, self)
        self.playlist.previous()

    def volumeChanged(self):
        self.player.setVolume(self.volume.value())

    def createPlaylist(self):
        self.playlist.clear()
        for i in range (0,len(self.files)):
            self.playlist.append(self.files[0])
        print(self.playlist)



    def timerEvent(self, e):
        self.step = self.step + 1
        self.playbar.setValue(self.step)
        if self.step>=1000 :
            self.step = 0 #재생바 종료
            self.step = self.step + 1
            self.playbar.setValue(self.step)
            return


         #재생바의 재생정도를 step값을 기준으로 함.

    def ShowPLayList(self):


        List = ['stay-PostMalon', '잠이 오질 않네요-장범준','Piano-melody_2', 'STAY-BLACKPINK','Piano-melody_1']
        for (i,j) in zip (List,range(10,110,20)):
            a = QLabel(i, self.showplaylist)
            a.move(10, j)



        self.showplaylist.setWindowTitle('PlayLIst')
        self.showplaylist.setWindowModality(Qt.ApplicationModal)
        self.showplaylist.setGeometry(1500, 400, 300, 200)
        self.showplaylist.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    main = Main()
    sys.exit(app.exec_())