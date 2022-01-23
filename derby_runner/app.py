# #############################################################################
# #############################################################################
import PyQt5
import feather
import pandas
import yaml
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
#


# ### BEGIN MAINWINDOW CLASS ###################################################

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


class MainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QTableView()
        self.title    = "Test"
# TODO:        self.iconname = "D:/_Qt/img/py-qt.png"
#        self.initWindow()

        self.model = pandasModel(df_stations)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)
        self.resize(1600, 1600)
        self.initWindow()

        def initWindow(self):
            self.setWindowTitle(self.title)
            self.setGeometry(100, 100, 500, 300)
            self.setWindowIcon(Gui.QIcon(self.iconname))
            self.qtMenu()

        def ymlread(self):
            global parent_str
            mfile = open("../resources/dr_menus.yml", "r")
            menusTxt: dict = yaml.safe_load(mfile)
            mfile.close()
#
            parent_level = 0
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

        def qtMenu(self):
            self.main_menu = self.menuBar().addMenu("&File")
            self.newItem = Wid.QAction("New", self, triggered=self.newFile)
            self.exitItem = Wid.QAction("Exit", self, triggered=Wid.qApp.quit)
            self.main_menu.addAction(self.newItem)
            self.main_menu.addAction(self.exitItem)

        def newFile(self):
            print("def newFile(self):")

        def openFileNameDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print(fileName)

        def openFile(self):
            # Logic for opening an existing file goes here...
            openFileNameDialog()
            self.centralWidget.setText("<b>File > Open...</b> clicked")

# ### END OF MAINWINDOW CLASS ################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
    sys.exit(app.exec_())
# ##############################################################################
# TODO: Add all of these menu options
# File Option: New
# File Option: Open
# File Option: Save
# File Option: Save As
# File Option: Rename
# File Option: Close
# File Option: Export
# File Option: Print
# File Option: Settings
# File Option: Exit
# #############################################################################
# findMenu = editMenu.addMenu("&Find and Replace")
# findMenu.addAction("Find")
# findMenu.addAction("Replace")
# #############################################################################
# Help Option: Getting Started
# Help Option: Search Help
# Help Option: Documentation
# Help Option: About

