import sys
import PyQt5.QtGui as Gui
import PyQt5.QtWidgets as Wid
import PyQt5.QtCore as Cor
import pandas

import PyQt5

import pyarrow.feather as feather
import pandas
import yaml

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView


def ymlread(x: str):
    mfile = open(x, "r")
    menusTxt: dict = yaml.safe_load(mfile)
    mfile.close()
    return (menusTxt)


event_columns = ['EventID', 'eName', 'eDescription', 'eStartDateTime', 'eEndDateTime']
df_events = pandas.DataFrame(columns=event_columns, index=[1, 2, 3, 4, 5])

stations_columns = ['StationID', 'sName', 'sDescription', 'TroopID', 'Primary\nAdultID',
                    'Secondary\nAdultID', 'Longitude', 'Latitude', 'EventID']
df_stations = pandas.DataFrame(columns=stations_columns, index=[1, 2, 3, 4, 5])

units_columns = ['UnitID', 'UnitType', 'UnitNumber', 'Leader1ID', 'Leader2ID', 'Leader3ID', 'ParticipateFlag',
                 'HostFlag', 'StationID']
df_units = pandas.DataFrame(columns=units_columns, index=[1, 2, 3, 4, 5])

squad_columns = ['SquadID', 'SquadType', 'SquadName', 'UnitID', 'SquadLeaderID']
df_squads = pandas.DataFrame(columns=squad_columns, index=[1, 2, 3, 4, 5])


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


class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title = "Dialogue"
        self.left = 1000
        self.top = 1200
        self.width = 1870
        self.height = 1480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


# +++
class Window(Wid.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        #        self.iconname = "D:/_Qt/img/py-qt.png"
        self.table = QTableView()
        self.mainnmenu = Wid.QMainWindow.menuBar(self)
        # self.qtMenu()
        # +++
        self.model = pandasModel(df_stations)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setCentralWidget(self.table)

    # +++
    def newFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getNewFileName(self, "QFileDialog.getNewFileName()", "",
                                                 "All Files (*);;Text Files (*.txt)", options=options)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "testText",
                                                  "All Files (*);;Python Files (*.py)", options=options)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)

    # +++

    def qtMenu(self):
        mainMenu = self.menuBar()
        pyGuiMenu = mainMenu.addMenu('&File')

        subItemTable = Wid.QAction('Open', self)
        subItemTable.setShortcut("Ctrl+O")
        subItemTable.setStatusTip("Open Window")
        subItemTable.triggered.connect(self.openFileDialog)  # +++
        pyGuiMenu.addAction(subItemTable)

    def newFileDialog(self):
        event_columns = ['EventID', 'eName', 'eDescription', 'eStartDateTime', 'eEndDateTime']
        df_events = pandas.DataFrame(columns=event_columns, index=[1, 2, 3, 4, 5])
        df_events.to_feather("/home/brickyard314/PycharmProjects/derby_runner/resources/events.ftr")

        stations_columns = ['StationID', 'sName', 'sDescription', 'TroopID', 'Primary\nAdultID',
                            'Secondary\nAdultID', 'Longitude', 'Latitude', 'EventID']
        df_stations = pandas.DataFrame(columns=stations_columns, index=[1, 2, 3, 4, 5])

        units_columns = ['UnitID', 'UnitType', 'UnitNumber', 'Leader1ID', 'Leader2ID', 'Leader3ID', 'ParticipateFlag',
                         'HostFlag', 'StationID']
        df_units = pandas.DataFrame(columns=units_columns, index=[1, 2, 3, 4, 5])

        squad_columns = ['SquadID', 'SquadType', 'SquadName', 'UnitID', 'SquadLeaderID']
        df_squads = pandas.DataFrame(columns=squad_columns, index=[1, 2, 3, 4, 5])

    def openFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/', "Image files (*.jpg *.gif)")

    def saveFileDialog(self):
        x = 1


def main():
    App = Wid.QApplication(sys.argv)
    homeWin = Window()
    homeWin.setWindowTitle("Derby Runner")
    left = 1000
    top = 1200
    width = 1870
    height = 1480
    homeWin.setGeometry(left, top, width, height)
    menus_text = ymlread("/home/brickyard314/PycharmProjects/derby_runner/resources/dr_menus.yml")

    parent_str = 'pyGuiMenu'
    for x in menus_text.values():
        for iKey, iValue in x.items():
            if iKey == "menulabel":
                exec("%s = %s" % (parent_str, "homeWin.menuBar().addMenu(iValue)"))

    Qmodel = pandasModel(df_squads)
    homeWin.table.setModel(Qmodel)

    sshFile = "myStyleSheet.qss"
    with open(sshFile, "r") as fh:
        homeWin.setStyleSheet(fh.read())

    homeWin.show()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
