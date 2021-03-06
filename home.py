from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QFrame, QTableWidget,QHeaderView, QTableWidgetItem, QVBoxLayout, QApplication,
                             QLabel,QLineEdit, QGroupBox, QFileDialog, QMainWindow, QStyledItemDelegate)
from main import *
import sys
import os

try:
    from html import escape
except ImportError:
    from cgi import escape


class HTMLDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HTMLDelegate, self).__init__(parent)
        self.doc = QtGui.QTextDocument(self)

    def paint(self, painter, option, index):
        substring = index.data(QtCore.Qt.UserRole)
        painter.save()
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        res = ""

        color = QtGui.QColor("orange")
        if substring:
            substrings = options.text.split(substring)
            res = """<font color="{}">{}</font>""".format(
                color.name(QtGui.QColor.HexRgb), substring
            ).join(list(map(escape, substrings)))
        else:
            res = escape(options.text)
        self.doc.setHtml(res)

        options.text = ""
        style = (
            QtWidgets.QApplication.style()
            if options.widget is None
            else options.widget.style()
        )
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, options, painter)

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        if option.state & QtWidgets.QStyle.State_Selected:
            ctx.palette.setColor(
                QtGui.QPalette.Text,
                option.palette.color(
                    QtGui.QPalette.Active, QtGui.QPalette.HighlightedText
                ),
            )
        else:
            ctx.palette.setColor(
                QtGui.QPalette.Text,
                option.palette.color(QtGui.QPalette.Active, QtGui.QPalette.Text),
            )

        textRect = style.subElementRect(QtWidgets.QStyle.SE_ItemViewItemText, options)

        if index.column() != 0:
            textRect.adjust(5,0,0,0,0)

        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(self.doc.idealWidth(), self.doc.size().height())

class Mp3Player(QWidget):

    def __init__(self,parent=None):
        super(Mp3Player,self).__init__(parent)
        self.initUI()


    def initUI(self):

        #button,title...
        self.logo = QPushButton() #추가버튼
        self.logo.setIcon(QtGui.QIcon('icon/logo.png'))
        self.logo.setIconSize(QtCore.QSize(50,50))

        name = QLabel(" H-music ") #mp3 이름(미정)
        name.setFont(QtGui.QFont("궁서",30,QtGui.QFont.Bold))
        name.setStyleSheet("Color : olive")
        self.playlist=[]

        self.search = QLineEdit() #검색
        font = self.search.font()
        font.setPointSize(20)
        self.setFont(font)
        self.search.setText("")

        self.searchbutton = QPushButton() #검색
        self.searchbutton.setIcon(QtGui.QIcon('icon/search.png'))
        self.searchbutton.setIconSize(QtCore.QSize(40,40))
        self.searchbutton.clicked.connect(self.searchkeyword)

        closebutton = QPushButton()#종료버튼
        closebutton.setIcon(QtGui.QIcon('icon/x.png'))
        closebutton.setIconSize(QtCore.QSize(50,50))
        closebutton.clicked.connect(app.quit)

        newbutton = QPushButton() #추가버튼
        newbutton.setIcon(QtGui.QIcon('icon/new.png'))
        newbutton.setIconSize(QtCore.QSize(50,50))
        newbutton.clicked.connect(self.addList)

        choosebutton = QPushButton()#리스트선택 후 넘어가기 버튼
        choosebutton.setIcon(QtGui.QIcon('icon/choose.png'))
        choosebutton.setIconSize(QtCore.QSize(50,50))
        choosebutton.clicked.connect(self.openwindow)

        #Layout
        v1box = QVBoxLayout() #playlist쪽 레이아웃
        v2box = QVBoxLayout() #버튼 모음 레이아웃

        # mp3 이름, 검색 창 레이아웃
        h2box = QHBoxLayout()
        h2box.addWidget(self.logo)
        h2box.addWidget(self.search)
        h2box.addWidget(self.searchbutton)

        #버튼 모음 세부 레이아웃
        v2_1box = QVBoxLayout()
        v2_2box = QVBoxLayout()
        v2_3box = QVBoxLayout()

        v1box.addLayout(h2box)

        #playlist 구성
        box = QVBoxLayout()
        playlist = QGroupBox("Play List")  # playlist를 담을곳
        v1box.addWidget(playlist)

        self.table =QTableWidget()
        self.table.setColumnCount(1)
        header = self.table.horizontalHeader()
        header.setFrameStyle(QFrame.Plain)
        header.setLineWidth(1)
        self.table.setHorizontalHeader(header)
        self.table.setHorizontalHeaderLabels(['노래목록'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setItemDelegate(HTMLDelegate(self.table))
        box.addWidget(self.table)

        playlist.setLayout(box)

        v2box.addLayout(v2_1box)
        v2box.addLayout(v2_2box)
        v2box.addLayout(v2_3box)

        v2_1box.addWidget(closebutton)
        v2_1box.addStretch(1)

        v2_3box.addStretch(1)
        v2_3box.addWidget(newbutton)
        v2_3box.addWidget(choosebutton)

        Main=QHBoxLayout()
        Main.addLayout(v1box)
        Main.addLayout(v2box)

        self.setLayout(Main)

        self.setWindowTitle('home')
        self.setGeometry(500, 200, 1000, 700)
        self.show()

    def addList(self):
        self.files = QFileDialog.getOpenFileNames(self,'Select one or more files to open','','Sound (*.mp3 *.wav *.ogg *.flac *.wma)')
        self.createPlaylist()
        a = self.files[0]
        path = a[0].split("music/")
        self.playlist.append(path[1])
        cnt = len(a)
        row = self.table.rowCount()
        self.table.setRowCount(row + cnt)
        for i in range(row, row + cnt):
            self.table.setItem(i, 0, QTableWidgetItem(path[1]))

    def createPlaylist(self):
        self.playlist.clear()
        a=self.files[0]
        path = a[0].split("music/")
        self.playlist.append(path[1])

    def searchkeyword(self):
        text = self.search.text()
        # clear
        allitems = self.table.findItems("", QtCore.Qt.MatchContains)
        selected_items = self.table.findItems(self.search.text(), QtCore.Qt.MatchContains)
        for item in allitems:
            item.setData(QtCore.Qt.UserRole, text if item in selected_items else None)

    def openwindow(self):
        self.hide()
        self.w = Main()
        self.w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp3 = Mp3Player()
    sys.exit(app.exec_())