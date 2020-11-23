import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,QLineEdit,QGroupBox)
from PyQt5 import QtCore, QtGui

class Home(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #button,title...
        name = QLabel(" 멋진이름 ") #mp3 이름(미정)
        name.setFont(QtGui.QFont("궁서",30,QtGui.QFont.Bold))
        name.setStyleSheet("Color : olive")

        searchbutton = QPushButton() #검색
        searchbutton.setIcon(QtGui.QIcon('../AD-Project6/icon/search.png'))
        searchbutton.setIconSize(QtCore.QSize(40,40))

        search = QLineEdit() #검색
        font = search.font()
        font.setPointSize(20)
        search.setFont(font)

        playlist = QGroupBox("Play List") #playlist를 담을곳

        closebutton = QPushButton()#종료버튼
        closebutton.setIcon(QtGui.QIcon('../AD-Project/icon/x.png'))
        closebutton.setIconSize(QtCore.QSize(50,50))
        upbutton = QPushButton() #위버튼
        upbutton.setIcon(QtGui.QIcon('../AD-Project/icon/up.png'))
        upbutton.setIconSize(QtCore.QSize(50,50))
        downbutton = QPushButton() #아래버튼
        downbutton.setIcon(QtGui.QIcon('../AD-Project/icon/down.png'))
        downbutton.setIconSize(QtCore.QSize(50,50))
        newbutton = QPushButton() #추가버튼
        newbutton.setIcon(QtGui.QIcon('../AD-Project/icon/new.png'))
        newbutton.setIconSize(QtCore.QSize(50,50))

        #Layout
        v1box = QVBoxLayout() #playlist쪽 레이아웃
        v2box = QVBoxLayout() #버튼 모음 레이아웃

        # mp3 이름, 검색 창 레이아웃
        v1_h1box = QHBoxLayout()
        v1_h1box.addWidget(name)
        v1_h1box.addWidget(search)
        v1_h1box.addWidget(searchbutton)

        #버튼 모음 세부 레이아웃
        v2_v1box = QVBoxLayout()
        v2_v2box = QVBoxLayout()
        v2_v3box = QVBoxLayout()


        v1box.addLayout(v1_h1box)
        v1box.addWidget(playlist)

        v2box.addLayout(v2_v1box)
        v2box.addLayout(v2_v2box)
        v2box.addLayout(v2_v3box)


        v2_v1box.addWidget(closebutton)
        v2_v1box.addStretch(1)

        v2_v2box.addWidget(upbutton)
        v2_v2box.addWidget(downbutton)

        v2_v3box.addStretch(1)
        v2_v3box.addWidget(newbutton)


        Homelayout=QHBoxLayout()
        Homelayout.addLayout(v1box)
        Homelayout.addLayout(v2box)

        self.setLayout(Homelayout)

        self.setWindowTitle('home')
        self.setGeometry(500, 200, 1000, 700)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    home = Home()
    sys.exit(app.exec_())
