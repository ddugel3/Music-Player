import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout,QFrame, QTableWidget,QHeaderView, QTableWidgetItem, QVBoxLayout, QApplication, QLabel,QLineEdit, QGroupBox, QFileDialog)
from PyQt5 import QtCore, QtGui


class Mp3Player(QWidget):

    def __init__(self):
        super().__init__()
        self.playlist=[]
        self.selectedList = [0]
        self.initUI()


    def initUI(self):
        #button,title...
        name = QLabel(" 멋진이름 ") #mp3 이름(미정)
        name.setFont(QtGui.QFont("궁서",30,QtGui.QFont.Bold))
        name.setStyleSheet("Color : olive")

        searchbutton = QPushButton() #검색
        searchbutton.setIcon(QtGui.QIcon('icon/search.png'))
        searchbutton.setIconSize(QtCore.QSize(40,40))
        searchbutton.clicked.connect(self.searchkeyword)

        search = QLineEdit() #검색
        font = search.font()
        font.setPointSize(20)
        search.setFont(font)

        closebutton = QPushButton()#종료버튼
        closebutton.setIcon(QtGui.QIcon('icon/x.png'))
        closebutton.setIconSize(QtCore.QSize(50,50))
        closebutton.clicked.connect(app.quit)

        upbutton = QPushButton() #위버튼
        upbutton.setIcon(QtGui.QIcon('icon/up.png'))
        upbutton.setIconSize(QtCore.QSize(50,50))

        downbutton = QPushButton() #아래버튼
        downbutton.setIcon(QtGui.QIcon('icon/down.png'))
        downbutton.setIconSize(QtCore.QSize(50,50))

        newbutton = QPushButton() #추가버튼
        newbutton.setIcon(QtGui.QIcon('icon/new.png'))
        newbutton.setIconSize(QtCore.QSize(50,50))
        newbutton.clicked.connect(self.addList)
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

        #playlist 구성
        box = QVBoxLayout()
        playlist = QGroupBox("Play List")  # playlist를 담을곳
        v1box.addWidget(playlist)

        self.table =QTableWidget(0,2,self)
        header = self.table.horizontalHeader()
        header.setFrameStyle(QFrame.Plain)
        header.setLineWidth(1)
        self.table.setHorizontalHeader(header)
        self.table.setHorizontalHeaderLabels(['파일명','블라블라,,,'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self.tableChanged)
        box.addWidget(self.table)
        playlist.setLayout(box)

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


    def tableChanged(self):
        self.selectedList.clear()
        for item in self.table.selectedIndexes():
            self.selectedList.append(item.row())

        self.selectedList = list(set(self.selectedList))


    def addList(self):
        files = QFileDialog.getOpenFileNames(self,'Select one or more files to open','','Sound (*.mp3 *.wav *.ogg *.flac *.wma)')
        cnt= len(files[0])
        row= self.table.rowCount()
        self.table.setRowCount(row + cnt)
        for i in range(row, row + cnt):
            self.table.setItem(i,0,QTableWidgetItem(files[0][i-row]))

        self.createPlaylist()

    def createPlaylist(self):
        self.playlist.clear()
        for i in range(self.table.rowCount()):
            self.playlist.append(self.table.item(i,0).text())
            str=(self.table.item(i, 0).text()).split("Desktop/")
            print(str[1])




    def searchkeyword(self):
        keyword = self.search.text()
        resultData = self.playlist[keyword]
        self.resultTable.setRowCount(len(resultData))
        row = 0
        for item in resultData:
            self.resultTable.setItem(row,0,QTableWidgetItem(keyword))
            self.resultTable.setItem(row, 1, QTableWidgetItem(item))
            row +=1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp3 = Mp3Player()
    mp3.show()
    sys.exit(app.exec_())