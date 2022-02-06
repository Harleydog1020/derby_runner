import sys
import pandas
import PyQt5
import yaml
import h5py

import testfunction as xf

import PyQt5.QtWidgets as Wid
import pyarrow.feather as feather

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView

# ##############################################################################

def ymlread(x: str):
    mfile = open(x, "r")
    menusTxt: dict = yaml.safe_load(mfile)
    mfile.close()
    return (menusTxt)

test_number = xf.testfunction(3)
print(test_number)
test_two = xf.testclass.test_two(input_number=3)
print(test_two)
# ##############################################################################
# CLASS TableModel - handles interaction of pandas dataframes with PyQt window
#
# ##############################################################################
class pandasModel(QAbstractTableModel):

    def __init__(self, data: object) -> object:
        QAbstractTableModel.__init__(self)
        self._data = data

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

# +++
class Window(Wid.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.fileName = None
        self.initUI()

    def initUI(self):

        stations_columns = ['StationID', 'sName', 'sDescription', 'TroopID', 'Primary\nAdultID',
                            'Secondary\nAdultID', 'Longitude', 'Latitude', 'EventID']
        self.df_stations = pandas.DataFrame(columns=stations_columns, index=[1, 2, 3, 4, 5])
        #        self.iconname = "D:/_Qt/img/py-qt.png"
        self.setWindowTitle("Derby Runner")
        left = 1000
        top = 1200
        width = 1870
        height = 1480
        self.setGeometry(left, top, width, height)

        menus_text = ymlread("/home/brickyard314/PycharmProjects/derby_runner/resources/dr_menus.yml")
        self.table = QTableView()
        self.mainnmenu = Wid.QMainWindow.menuBar(self)
        self.setCentralWidget(self.table)

        Qmodel = pandasModel(self.df_stations)
        self.table.setModel(Qmodel)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.menuBar = Wid.QMainWindow.menuBar(self)

        File = self.menuBar.addMenu("&File")

        New = File.addAction('&New')
        New.triggered.connect(lambda: self.newFileDialog())

        Open = File.addAction('&Open')
        Open.triggered.connect(lambda: self.openFileDialog())

        Save = File.addAction('&Save')
        Save.triggered.connect(lambda: self.saveFileDialog())

        Edit = self.menuBar.addMenu("&Edit")

        sshFile = "../resources/derby_runner.stylesheet"
        with open(sshFile, "r") as fh:
            x = self.setStyleSheet(fh.read())

        self.newEvent()

    def Ui_setup(self, data):
        self.centralwidget = QtWidgets.QMainWindow
#        self.centralwidget.setObjectName(, "centralwidget")
        self.table = QtWidgets.QTableView()
        self.table.setGeometry(QtCore.QRect(0, 0, 256, 192))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setMaximumSize(QtCore.QSize(1000, 1000))

        self.newEvent()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        newAct = QAction(QIcon('~/PycharmProjects/derby_runner/resources/icons/notebook--plus.png'), '&New', self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('Create a New Event')
        newAct.triggered.connect(self.newEvent)

        openAct = QAction(QIcon('~/PycharmProjects/derby_runner/resources/icons/notebook--plus.png'), '&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open an Event')
        openAct.triggered.connect(self.openFileNameDialog)
        fileMenu.addAction((openAct))

        saveAct = QAction(QIcon('~/PycharmProjects/derby_runner/resources/icons/notebook--plus.png'), '&Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Save an Event')
        saveAct.triggered.connect(self.saveFileDialog)
        fileMenu.addAction((saveAct))

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAct)

        editMenu = menubar.addMenu('&Edit')
        cutAct = QAction('Cu&t', self)
        cutAct.setShortcut('Ctrl+X')
        cutAct.setStatusTip('Cut highlighted')
        editMenu.addAction(cutAct)

        copyAct = QAction('&Copy', self)
        copyAct.setShortcut('Ctrl+C')
        copyAct.setStatusTip('Copy highlighted')
        editMenu.addAction(copyAct)

        pasteAct = QAction('&Paste', self)
        pasteAct.setShortcut('Ctrl-V')
        pasteAct.setStatusTip('Paste from clipboard')
        editMenu.addAction((pasteAct))

        deleteAct = QAction('&Delete', self)
        deleteAct.setShortcut('Delete')
        deleteAct.setStatusTip('Delete highlighted')
        editMenu.addAction(deleteAct)

        viewMenu = menubar.addMenu('&View')
        waypointsAct = QAction('&Waypoints', self)
        waypointsAct.setShortcut('Ctrl+W')
        waypointsAct.setStatusTip('Switch to Waypoints Table')
        viewMenu.addAction(waypointsAct)
        waypointsAct.triggered.connect(self.viewWay)

        stationsAct = QAction('&Stations', self)
        stationsAct.setShortcut('Ctrl+S')
        stationsAct.setStatusTip('Switch to Stations Table')
        viewMenu.addAction(stationsAct)
        stationsAct.triggered.connect(self.viewStt)

        coursesAct = QAction('&Courses', self)
        coursesAct.setShortcut('Ctrl+C')
        coursesAct.setStatusTip('Switch to Courses Table')
        viewMenu.addAction(coursesAct)
        coursesAct.triggered.connect(self.viewCou)

        unitsAct = QAction('&Units', self)
        unitsAct.setShortcut('Ctrl+U')
        unitsAct.setStatusTip('Switch to Units Table')
        viewMenu.addAction(unitsAct)
        unitsAct.triggered.connect(self.viewUnt)

    def openFileDialog(self,):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,
                                                       caption="Open File",
                                                       directory= "../resources/",
                                                       filter="All Files (*);;Python Files (*.py)",
                                                       options=options)
        if self.fileName[0]:
            self.df_events = pandas.read_hdf(self.fileName, key="events")
#            print(df_events)
            self.model = pandasModel(self.df_events)
            self.table.setModel(self.model)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.setCentralWidget(self.table)

    def saveFileDialog(self,):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', '../resources/', "Python Files (*.py);;All Files (*)",
                                               options=QFileDialog.DontUseNativeDialog)
        if self.fileName[0]:
            self.df_events = self.df_events.astype(str)
            self.df_events.to_hdf(self.fileName, key='events', mode='w')
            return 0

if __name__ == "__main__":
    app = Wid.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
