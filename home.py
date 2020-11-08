import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,QLineEdit,QGroupBox)
from PyQt5 import QtCore, QtGui

class Mp3Player(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #button,title...
        name = QLabel(" 멋진이름 ") #mp3 이름(미정)
        name.setFont(QtGui.QFont("궁서",30,QtGui.QFont.Bold))
        name.setStyleSheet("Color : olive")

        searchbutton = QPushButton() #검색
        searchbutton.setIcon(QtGui.QIcon('search.png'))
        searchbutton.setIconSize(QtCore.QSize(40,40))

        search = QLineEdit() #검색
        font = search.font()
        font.setPointSize(20)
        search.setFont(font)

        playlist = QGroupBox("Play List") #playlist를 담을곳

        closebutton = QPushButton()#종료버튼
        closebutton.setIcon(QtGui.QIcon('x.png'))
        closebutton.setIconSize(QtCore.QSize(50,50))
        upbutton = QPushButton() #위버튼
        upbutton.setIcon(QtGui.QIcon('up.png'))
        upbutton.setIconSize(QtCore.QSize(50,50))
        downbutton = QPushButton() #아래버튼
        downbutton.setIcon(QtGui.QIcon('down.png'))
        downbutton.setIconSize(QtCore.QSize(50,50))
        newbutton = QPushButton() #추가버튼
        newbutton.setIcon(QtGui.QIcon('new.png'))
        newbutton.setIconSize(QtCore.QSize(50,50))

        #Layout
        v1box = QVBoxLayout() #playlist쪽 레이아웃
        v2box = QVBoxLayout() #버튼 모음 레이아웃

        # mp3 이름, 검색 창 레이아웃
        h2box = QHBoxLayout()
        h2box.addWidget(name)
        h2box.addWidget(search)
        h2box.addWidget(searchbutton)

        #버튼 모음 세부 레이아웃
        v2_1box = QVBoxLayout()
        v2_2box = QVBoxLayout()
        v2_3box = QVBoxLayout()


        v1box.addLayout(h2box)
        v1box.addWidget(playlist)

        v2box.addLayout(v2_1box)
        v2box.addLayout(v2_2box)
        v2box.addLayout(v2_3box)


        v2_1box.addWidget(closebutton)
        v2_1box.addStretch(1)

        v2_2box.addWidget(upbutton)
        v2_2box.addWidget(downbutton)

        v2_3box.addStretch(1)
        v2_3box.addWidget(newbutton)


        Main=QHBoxLayout()
        Main.addLayout(v1box)
        Main.addLayout(v2box)

        self.setLayout(Main)

        self.setWindowTitle('home')
        self.setGeometry(500, 200, 1000, 700)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp3 = Mp3Player()
    sys.exit(app.exec_())