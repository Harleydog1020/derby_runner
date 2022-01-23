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
x = "../resources/dr_menus.yml"

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
        super(Window, self).__init__();
        self.title    = "Test"
#        setGeometry(100, 100, 500, 300)
        self.table = QTableView()
        self.iconname = "D:/_Qt/img/py-qt.png"
        menusTxt: dict = self.ymlread(x)
        self.initWindow(menusTxt)
# +++
        self.model = pandasModel(df_stations)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
# +++
    def ymlread(self, x):
        global parent_str
        mfile = open(x, "r")
        menusTxt: dict = yaml.safe_load(mfile)
        mfile.close()
        return(menusTxt)

    def initWindow(self, menusTxt):
        self.setWindowTitle(self.title)
        self.setWindowIcon(Gui.QIcon(self.iconname))
        self.qtMenu(menusTxt)

    def qtMenu(self,menusTxt):
        global parent_str
        for x in menusTxt.values():
            for iKey, iValue in x.items():
                if iKey == "menulabel":
                    parent_str = iValue.strip('&') + "Menu"
                    exec("%s = %s" % (parent_str, "menuBar.addMenu(iValue)"))
                else:
                    child_str = parent_str + ".addAction(\"" + iValue + "\")"
                    exec("%s" % (child_str))
                    child_str = parent_str + ".newAction.triggered.connect(self." + iValue.lower() + parent_str + ")"
                    exec("%s" % (child_str))

    def OLDqtMenu(self):
        self.main_menu = self.menuBar().addMenu("&File")
        self.newItem  = Wid.QAction("New",  self,  triggered = self.newFile)
        self.exitItem = Wid.QAction("Exit", self, triggered = Wid.qApp.quit)
        self.main_menu.addAction(self.newItem)
        self.main_menu.addAction(self.exitItem)

    def newFile(self):
        print("def newFile(self):")


if __name__ == '__main__':
    app = Wid.QApplication(sys.argv)
    qt_app = Window()
    qt_app.show()
    sys.exit(app.exec_())