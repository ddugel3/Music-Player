from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QFrame, QTableWidget,QHeaderView, QTableWidgetItem, QVBoxLayout, QApplication,
                             QLabel,QLineEdit, QGroupBox, QFileDialog,QStyledItemDelegate)
from PyQt5 import QtCore, QtGui,QtWidgets
import sys

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

        thefuckyourshitup_constant = 1
        margin = (option.rect.height() - options.fontMetrics.height()) // 2
        margin = margin - thefuckyourshitup_constant
        textRect.setTop(textRect.top() + margin)

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
        name = QLabel(" 멋진이름 ") #mp3 이름(미정)
        name.setFont(QtGui.QFont("궁서",30,QtGui.QFont.Bold))
        name.setStyleSheet("Color : olive")
        self.playlist=[]
        self.selectedList = [0]

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

        self.table =QTableWidget(0,1,self)
        header = self.table.horizontalHeader()
        header.setFrameStyle(QFrame.Plain)
        header.setLineWidth(1)
        self.table.setHorizontalHeader(header)
        self.table.setHorizontalHeaderLabels(['노래목록'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self.tableChanged)
        self.table.setItemDelegate(HTMLDelegate(self.table))
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
            str= (self.table.item(i,0).text()).split("home/been/문서/GitHub/AD-Project/MUSIC/")
            self.playlist.append(str[1])
            print(str[1])


    def searchkeyword(self):
        text = self.search.text()
        # clear
        allitems = self.table.findItems("", QtCore.Qt.MatchContains)
        selected_items = self.table.findItems(self.search.text(), QtCore.Qt.MatchContains)
        for item in allitems:
            item.setData(QtCore.Qt.UserRole, text if item in selected_items else None)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp3 = Mp3Player()
    mp3.show()
    sys.exit(app.exec_())