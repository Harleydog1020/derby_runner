import sys
import PyQt5.QtGui     as Gui
import PyQt5.QtWidgets as Wid
import PyQt5.QtCore    as Cor
import pandas

import PyQt5
import feather
import pandas
import yaml

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon

data = [['Alex',10],['Bob',12],['Clarke',13]]
df_stations = pandas.DataFrame(data,columns=['Name','Age'])


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

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]


class Window(Wid.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.title    = "Test"
        self.table = QTableView()
        self.iconname = "D:/_Qt/img/py-qt.png"

        menusTxt = self.ymlread("/home/brickyard314/PycharmProjects/derby_runner/resources/dr_menus.yml")
        self.initWindow(menusTxt)

# +++
        self.model = pandasModel(df_stations)
        self.table.setModel(self.model)
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
    def ymlread(self, x: str):
        global parent_str
        mfile = open(x, "r")
        menusTxt: dict = yaml.safe_load(mfile)
        mfile.close()
        return(menusTxt)

    def initWindow(self, menusTxt):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 500, 300)
        self.setWindowIcon(Gui.QIcon(self.iconname))
        self.qtMenu(menusTxt)

    def qtMenu(self, menusTxt: dict):
        global parent_str
        for x in menusTxt.values():
            for iKey, iValue in x.items():
                if iKey == "menulabel":
                    parent_str = iValue.strip('&') + "Dialog"
                    exec("%s = %s" % (parent_str, "self.menuBar().addMenu(iValue)"))
                else:
                    child_str = iValue.strip('&').lower() + "Action = PyQt5.QtWidgets.QAction('" + iValue.strip('&') + "', self)"
                    print(child_str)
                    exec("%s" % (child_str))

                    child_str = parent_str + ".addAction(\"" + iValue + "\")"
                    print(child_str)
                    exec("%s" % (child_str))

                    child_str = iValue.strip('&').lower() + "Action.triggered.connect(self." + iValue.strip('&').lower() + parent_str + ")"
                    print(child_str)
                    exec("%s" % (child_str))

if __name__ == '__main__':

    app = Wid.QApplication(sys.argv)
    qt_app = Window()
    qt_app.show()
    sys.exit(app.exec_())