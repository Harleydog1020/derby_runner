import sys
import pandas
import PyQt5
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtWidgets import QApplication, QTableWidget
from PyQt5.QtCore import QAbstractTableModel, Qt

stations_columns = ['StationID', 'sName', 'sDescription', 'TroopID', 'Primary\nAdultID', 'Secondary\nAdultID',
                    'Longitude', 'Latitude', 'EventID']
df_stations = pandas.DataFrame(columns=stations_columns, index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = pandasModel(df_stations)
    view = QTableView()
#    view.button_add_c = QtWidgets.QPushButton('add column')
#    view.button_add_c.clicked.connect(self.click_button_add_c)
    view.setModel(model)
    stylesheet = "QHeaderView::section{Background-color:rgb(190,190,190); background-color: #87CEFA;  border - radius: 14px; font: 18px}"
    view.setStyleSheet(stylesheet)
    view.setAlternatingRowColors(True)
 #   view.setHorizontalHeader(['Station ID', 'Station Name', 'Station\nDescription', 'TroopID', 'Primary\nAdultID', 'Secondary\nAdultID',
                    'Longitude', 'Latitude', 'EventID'])
#    view.setHorizontalHeaderLabels(['Station ID', 'Station Name', 'Station\nDescription', 'TroopID', 'Primary\nAdultID', 'Secondary\nAdultID',
#                    'Longitude', 'Latitude', 'EventID'])
    view.resize(1600, 1600)
    view.show()
    sys.exit(app.exec_())