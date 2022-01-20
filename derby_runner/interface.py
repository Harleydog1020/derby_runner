import sys
import PyQt5
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QToolBar, QAction, QStatusBar, QCheckBox, QMenu,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import yaml

class MainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        global parent_str
        super().__init__()

        mfile = open("../resources/dr_menus.yml", "r")
        menusTxt: dict = yaml.safe_load(mfile)
        mfile.close()

        self.setWindowTitle("Derby Runner")

        menuBar = self.menuBar()
        menuBar.setStyleSheet("font: 18px ")
        parent_level = 0
        for x in menusTxt.values():
            for iKey, iValue in x.items():
                if iKey == "menulabel":
                    parent_str = iValue.strip('&') + "Menu"
                    exec("%s = %s" % (parent_str, "menuBar.addMenu(iValue)"))
                else:
                    child_str = parent_str + ".addAction(\"" + iValue + "\")"
                    exec("%s" % (child_str))
#                    fileMenu.addAction(iValue)

#        findMenu = editMenu.addMenu("&Find and Replace")
#        findMenu.addAction("Find")
#        findMenu.addAction("Replace")

app = QApplication(sys.argv[1:])
w = MainWindow()
w.resize(1280,720)
w.show()
app.exec()