import sys
import pandas
import PyQt5
from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow
from PyQt5.QtWidgets import QApplication, QTableWidget
from PyQt5.QtCore import QAbstractTableModel, Qt

stationsFile = "../resources/stations.ftr"
df_stations = pandas.read_feather(stationsFile)

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #    view.button_add_c = QtWidgets.QPushButton('add column')
        #    view.button_add_c.clicked.connect(self.click_button_add_c)
        #    view.setHorizontalHeader(['Station ID', 'Station Name', 'Station\nDescription', 'TroopID', 'Primary\nAdultID', 'Secondary\nAdultID', 'Longitude', 'Latitude', 'EventID'])
        #    view.setHorizontalHeaderLabels(['Station ID', 'Station Name', 'Station\nDescription', 'TroopID', 'Primary\nAdultID', 'Secondary\nAdultID', 'Longitude', 'Latitude', 'EventID'])

        self.table = QTableView()

        self.model = pandasModel(df_stations)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        stylesheet = "QHeaderView::section{Background-color:rgb(190,190,190); background-color: #87CEFA;  border - radius: 14px; font: 18px}"
        self.setStyleSheet(stylesheet)
        self.resize(1600, 1600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    print(df_stations)
    df_stations.to_feather(stationsFile)
