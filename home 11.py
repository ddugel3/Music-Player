from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QFrame, QTableWidget,QHeaderView, QTableWidgetItem, QVBoxLayout, QApplication,
                             QLabel,QLineEdit, QGroupBox, QFileDialog, QMainWindow, QStyledItemDelegate)
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
        self.logo = QPushButton() #추가버튼
        self.logo.setIcon(QtGui.QIcon('icon/logo.png'))
        self.logo.setIconSize(QtCore.QSize(50,50))

        name = QLabel(" H-music ") #mp3 이름(미정)
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

        newbutton = QPushButton() #추가버튼
        newbutton.setIcon(QtGui.QIcon('icon/new.png'))
        newbutton.setIconSize(QtCore.QSize(50,50))
        newbutton.clicked.connect(self.addList)

        choosebutton = QPushButton()#리스트선택 후 넘어가기 버튼
        choosebutton.setIcon(QtGui.QIcon('icon/choose.png'))
        choosebutton.setIconSize(QtCore.QSize(50,50))
        choosebutton.clicked.connect(self.window2)

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
        self.table.setRowCount(20)
        self.table.setColumnCount(1)
        self.setTableData()
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

    def setTableData(self):
        self.table.setItem(0,0,QTableWidgetItem("Make a wish.mp3"))
        self.table.setItem(0,1,QTableWidgetItem("cheer up.mp3"))
        self.table.setItem(0,2,QTableWidgetItem("snowman.mp3"))
        self.table.setItem(0,3,QTableWidgetItem("santa tell me.mp3"))
        self.table.setItem(0,4,QTableWidgetItem("text me merry chirstmas.mp3"))
        self.table.setItem(0,5,QTableWidgetItem("black out.mp3"))
        self.table.setItem(0,6,QTableWidgetItem("perhaps love.mp3"))
        self.table.setItem(0,7,QTableWidgetItem("fly.mp3"))
        self.table.setItem(0,8,QTableWidgetItem("what are we.mp3"))
        self.table.setItem(0,9,QTableWidgetItem("thunder.mp3"))
        self.table.setItem(0,10,QTableWidgetItem("adios.mp3"))
        self.table.setItem(0,11,QTableWidgetItem("RBB.mp3"))
        self.table.setItem(0,12,QTableWidgetItem("aside.mp3"))
        self.table.setItem(0,13,QTableWidgetItem("hug.mp3"))
        self.table.setItem(0,14,QTableWidgetItem("savage love.mp3"))
        self.table.setItem(0,15,QTableWidgetItem("my page.mp3"))
        self.table.setItem(0,16,QTableWidgetItem("square.mp3"))
        self.table.setItem(0,17,QTableWidgetItem("welcome to my playground.mp3"))
        self.table.setItem(0,18,QTableWidgetItem("i can't stop me.mp3"))
        self.table.setItem(0,19,QTableWidgetItem("what is love?.mp3"))
        self.table.setItem(0,20,QTableWidgetItem("solo.mp3"))

    def addList(self):
        self.files = QFileDialog.getOpenFileNames(self,'Select one or more files to open','','Sound (*.mp3 *.wav *.ogg *.flac *.wma)')
        Str =str(self.files[0]).split("/")
        Str1=Str[len(Str) -1].split(("."))
        self.playlist.append(Str1[1])
        cnt= len(self.files[0])
        row= self.table.rowCount()
        self.table.setRowCount(row + cnt)
        for i in range(row, row + cnt):
            self.table.setItem(i,0,QTableWidgetItem(self.files[0][i-row]))
        self.createPlaylist()

    def createPlaylist(self):
        self.playlist.clear()
        self.playlist.append(self.files[0])
        print(self.playlist)

    def searchkeyword(self):
        text = self.search.text()
        # clear
        allitems = self.table.findItems("", QtCore.Qt.MatchContains)
        selected_items = self.table.findItems(self.search.text(), QtCore.Qt.MatchContains)
        for item in allitems:
            item.setData(QtCore.Qt.UserRole, text if item in selected_items else None)

    def window2(self):
        self.w = Window2()
        self.w.show()
        self.hide()
#///////////////////////////////////// main ///////////////////////////////////
class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window22222")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp3 = Mp3Player()
    mp3.show()
    sys.exit(app.exec_())