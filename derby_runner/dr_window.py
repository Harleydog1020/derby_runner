import sys
import pandas
import PyQt5
import yaml

import testfunction as xf

import PyQt5.QtWidgets as Wid
import pyarrow.feather as feather

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView


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

        #        self.iconname = "D:/_Qt/img/py-qt.png"
        self.table = QTableView()
        self.mainnmenu = Wid.QMainWindow.menuBar(self)
        # self.qtMenu()
        # +++
        self.model = pandasModel(df_stations)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setCentralWidget(self.table)

    def newFileDialog(self):
        x = 1

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "testText",
                                                  "All Files (*);;Python Files (*.py)", options=options)

    def saveFileDialog(self):
        x = 1
