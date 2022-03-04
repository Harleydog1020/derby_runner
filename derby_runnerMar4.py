import sys
import time
import datetime
import dr_utils as dru
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QFileDialog, QVBoxLayout, QLabel, QFrame,
    QApplication, QToolBar, QAction, QMenuBar, QSplitter, QProgressBar
)
import atexit
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QWidget
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        self.draw()
# ##############################################################################
# CLASS Color - test widget
# ##############################################################################
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

###############################################################################################
class NewModel(QtCore.QAbstractTableModel):
    def __init__(self, data: object) -> object:
        super(NewModel, self).__init__()
        self.data = data

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = self.data.iloc[index.row(), index.column()]
            return str(value)

    def setData(self, index, value, role=Qt.DisplayRole, **kwargs):
        if role == Qt.EditRole:
            self.data.iloc[index.row(), index.column()] = value
            print("Value = " + str(value))
            return True
        else:
            value = self.data.iloc[index.row(), index.column()]
            print("contents = " + str(value))
            return True
        return False

    def rowCount(self, index=QtCore.QModelIndex()) -> int:
        return self.data.shape[0]

    def columnCount(self, index=QtCore.QModelIndex()) -> int:
        return self.data.shape[1]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])
            if orientation == Qt.Vertical:
                return str(self.data.index[section])


##############################################################################################
class Delegate(QtWidgets.QItemDelegate):
    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices

    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QComboBox(parent)
        self.editor.addItems(self.items)
        return self.editor

    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.EditRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class PlainTextEditDelegate(QtWidgets.QItemDelegate):
    def __init__(self, owner):
        super().__init__(owner)

    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QPlainTextEdit(parent)
        return self.editor

    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QPlainTextEdit()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl( opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)

def goodbye(data):
    print(data)
    print('Goodbye')


#######################################################################
class MainWindow(QtWidgets.QMainWindow):
    """
    A class to set up and maintain the GUI interface for Derby Runner

    Attributes
    ----------
    layout_main : object
        description
    splitter_main : object
        description

    Methods
    -------
    setup_ui():
        .
    show_data():
        .
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.df_adults = None
        self.df_coursepoints = None
        self.df_courses = None
        self.df_itineraries = None
        self.df_schedules = None
        self.df_stations = None
        self.df_squads = None
        self.df_units = None
        self.df_waypoints = None
        self.df_youths = None

        dru.init_lists(self)
        self.new_event()

        self.current_filename = '[Untitled]'
        self.data_status = 'Unsaved'
        self.current_table = 'units'
        self.setWindowTitle("Derby Runner - " + self.current_filename)
        self.layout_main = QHBoxLayout()
        self.splitter_main = QSplitter(Qt.Horizontal)
        self.splitter_data = QSplitter(Qt.Vertical)
        self.splitter_utils = QSplitter(Qt.Vertical)
        self.menu_bar = QMenuBar()
        self.statusBar().showMessage('Welcome to Derby Runner.')
        self.data_tools = QToolBar()
        self.table = QtWidgets.QTableView()
        self.table.resizeColumnsToContents()
        self.table.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 0px; margin: 0px; border: 0px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        self.model = NewModel
        self.mapwidget = PlotCanvas(self)
        self.layout_main.setContentsMargins(5, 5, 5, 5)
        self.layout_main.setSpacing(20)
        self.splitter_main.addWidget(self.splitter_data)
        self.splitter_main.addWidget(self.splitter_utils)
        self.layout_main.addWidget(self.splitter_main)

        self.setup_ui()

    def show_data(self):
        print("show_data: ")
        print(self.df2)

    def add_row(self):
        rows = sorted(set(index.row() for index in
                          self.table.selectedIndexes()))
        print(len(rows))
        for row in rows:
            print('Row %d is selected' % row)
        #if no rows selected, add one row to the end
        if (len(rows) == 0):
            unit_row = pd.DataFrame(columns=self.units_columns, index=[0])
            unit_row.fillna('  ', inplace=True)
            self.df_units = self.df_units.append(unit_row, ignore_index=True)
            self.model = NewModel(self.df_units)
            self.table.setModel(self.model)
        else:
            unit_row = pd.DataFrame(columns=self.units_columns, index=range(len(rows)))
            unit_row.fillna('  ', inplace=True)
            self.df_units = self.df_units.append(unit_row, ignore_index=True)
            self.model = NewModel(self.df_units)
            self.table.setModel(self.model)

    def del_row(self):
        rows = sorted(set(index.row() for index in
                          self.table.selectedIndexes()))
        print(len(rows))
        for row in rows:
            print('Row %d is selected' % row)

        #if no rows selected, popup "no rows selected"
        #if 1 or more selected, delete rows selected

    def copy_row(self):
        rows = sorted(set(index.row() for index in
                          self.table.selectedIndexes()))
        print(len(rows))
        for row in rows:
            print('Row %d is selected' % row)

        #if no rows selected, popup "no rows selected"
        # if 1 or more selected, copy to temp DF then add below last row

    def settings_dialog(self):
        dlg = QtWidgets.QDialog()
        self.layout_main.addWidget(self.comboBox)
        self.comboBox.addItem("Navy")
        self.comboBox.addItem("Gray")
        self.comboBox.addItem("Blue")
        x = self.comboBox.currentText()
        ssh_file = "/home/brickyard314/PycharmProjects/derby_runner/derby_runner/style_gray.css"
        fh_style = open(ssh_file, "r").read()
        MainWindow.setStyleSheet(fh_style)
        if x == 'Gray':
            ssh_file = "/home/brickyard314/PycharmProjects/derby_runner/derby_runner/style_gray.css"
            with open(ssh_file, "r") as fh:
                MainWindow.setStyleSheet(fh.read())
        elif x == 'Blue':
            print('blue is the sky')
            ssh_file = "/home/brickyard314/PycharmProjects/derby_runner/derby_runner/style_blue.css"
            with open(ssh_file, "r") as fh:
                MainWindow.setStyleSheet(fh.read())
        else:
            print('it is just dark')

        dlg.setGeometry(1000, 1000, 500, 500)
        dlg.setLayout(self.layout_main)
        dlg.exec()

    def new_event(self):
        self.df_units = dru.init_units(self)
        self.df_stations = dru.init_stations(self)
        self.df_waypoints = dru.init_waypoints(self)
        self.df_courses = dru.init_courses(self)
        self.df_coursepoints = dru.init_coursepoints(self)
        self.df_adults = dru.init_adults(self)
        self.df_youths = dru.init_youths(self)
        self.df_itineraries = dru.init_itineraries(self)
        self.df_schedules = dru.init_schedules(self)
        self.df_squads = dru.init_squads(self)

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        x = QFileDialog()
        file_name, _ = x.getSaveFileName(caption="Caption", filter="H5F Files (*.h5);;All Files (*)", options=options)
        file_name = file_name
        if file_name:
            self.df_stations.to_hdf(file_name, key='stations', mode='w')
            self.df_waypoints.to_hdf(file_name, key='waypoints', mode='a')
            self.df_courses.to_hdf(file_name, key='courses', mode='a')
            self.df_coursepoints.to_hdf(file_name, key='coursepoints', mode='a')
            self.df_units.to_hdf(file_name, key='units', mode='a')
            self.df_squads.to_hdf(file_name, key='squads', mode='a')
            self.df_itineraries.to_hdf(file_name, key='itineraries', mode='a')
            self.df_schedules.to_hdf(file_name, key='schedules', mode='a')
            self.df_youths.to_hdf(file_name, key='youths', mode='a')
            self.df_adults.to_hdf(file_name, key='adults', mode='a')

        self.current_filename = file_name
        return

    def open_filename_dialog(self):
        x = QFileDialog()
        x.setGeometry(500, 500, 1000, 1500)

        file_name, _ = x.getOpenFileName(caption="Open Derby Runner files",
                                         filter="H5F Files (*.h5);;All Files (*)")
        if file_name:

            self.df_stations = pd.read_hdf(file_name, key='stations', mode='r')
            self.df_waypoints = pd.read_hdf(file_name, key='waypoints', mode='r')
            self.df_courses = pd.read_hdf(file_name, key='courses', mode='r')
            self.df_coursepoints = pd.read_hdf(file_name, key='coursepoints', mode='r')
            self.df_schedules = pd.read_hdf(file_name, key='schedules', mode='r')
            self.df_itineraries = pd.read_hdf(file_name, key='itineraries', mode='r')
            self.df_units = pd.read_hdf(file_name, key='units', mode='r')
            self.df_squads = pd.read_hdf(file_name, key='squads', mode='r')
            self.df_youths = pd.read_hdf(file_name, key='youths', mode='r')
            self.df_adults = pd.read_hdf(file_name, key='adults', mode='r')
            self.change_model('units')
            self.table.resizeColumnsToContents()

        self.current_filename = file_name
        return

    def change_model(self, table_name):
        if table_name == 'waypoints':
            self.model = None
            self.current_table = 'waypoints'
            self.model = NewModel(self.df_waypoints)
            self.table.setModel(self.model)

        elif table_name == 'stations':
            self.model = None
            self.current_table = 'stations'
            self.model = NewModel(self.df_stations)
            self.table.setModel(self.model)
        elif table_name == 'courses':
            self.model = None
            self.current_table = 'courses'
            self.model = NewModel(self.df_courses)
            self.table.setModel(self.model)
        elif table_name == 'coursepoints':
            self.model = None
            self.current_table = 'coursepoints'
            self.model = NewModel(self.df_coursepoints)
            self.table.setModel(self.model)
        elif table_name == 'schedules':
            self.model = None
            self.current_table = 'schedules'
            self.model = NewModel(self.df_schedules)
            self.table.setModel(self.model)
        elif table_name == 'itineraries':
            self.model = None
            self.current_table = 'itineraries'
            self.model = NewModel(self.df_itineraries)
            self.table.setModel(self.model)
        elif table_name == 'units':
            self.model = None
            self.current_table = 'units'
            self.model = NewModel(self.df_units)
            self.table.setModel(self.model)
        elif table_name == 'squads':
            self.model = None
            self.current_table = 'squads'
            self.model = NewModel(self.df_squads)
            self.table.setModel(self.model)
        elif table_name == 'adults':
            self.model = None
            self.current_table = 'adults'
            self.model = NewModel(self.df_adults)
            self.table.setModel(self.model)
        elif table_name == 'youths':
            self.model = None
            self.current_table = 'youths'
            self.model = NewModel(self.df_youths)
            self.table.setModel(self.model)
        else:
            self.current_table = 'oops'
            self.model = NewModel(self.df_stations)
            self.table.setModel(self.model)

        self.table.resizeColumnsToContents()
        return

    def setup_ui(self):
        '''Assembles all of the pieces for the Main Window'''

        data2 = [['10', 'Alex'], ['12', 'Bob'], ['13', 'Clarke']]
        self.df2 = pd.DataFrame(data2, columns=['Age', 'Name'])
        arrayA = np.array([-75.42579, -75.42947, -75.42807])
        arrayB = np.array([40.3662, 40.36383, 40.36088])
        image = Image.open('/home/brickyard314/DerbyRunner/map.png', 'r')  # Load map image.

        ax = self.mapwidget.figure.add_subplot(111)
        ax.plot(arrayA, arrayB, 'o')
        ax.set_xticks([-75.42, -75.425, -75.43])
        ax.set_yticks([40.36, 40.365, 40.37])
        im = ax.imshow(image, extent=[-75.42, -75.43, 40.36, 40.37])

        if self.current_table == 'adults':
            print("Adults")
        elif self.current_table == 'units':
            choices =  self.unit_types
            self.model = NewModel(self.df_units)
        else:
            choices = ['Alex', 'Bob', 'Clarke', 'Ship', 'Troop', 'Other']
            self.model = NewModel(self.df2)

        self.table.setModel(self.model)

        ### TOOL BAR ############################################################
        #Qt themes work on all platforms, it's just that on Linux you get the theme for free.
        # On non-Linux platforms you have to define your own icon theme from scratch.
        # However, this is only really worth doing if you want to have a Linux-native look,
        # for other use cases the QResource system is simpler.

        cut_icon = QtGui.QIcon.fromTheme("edit-cut")
        copy_icon = QtGui.QIcon.fromTheme("edit-copy")
        paste_icon = QtGui.QIcon.fromTheme("edit-paste")
        delete_icon = QtGui.QIcon.fromTheme("edit-delete")
        insert_icon = QtGui.QIcon.fromTheme("list-add")
        #Select Row .../table-select-row
        #import_icon = QtGui.QIcon.fromTheme("")
        #Export ".../document-export.png
        icon = QtGui.QIcon.fromTheme("document-new")
        button1_action = QAction(cut_icon, "Cut Row", self)
        button1_action.setCheckable(False)

        self.data_tools.addAction(button1_action)
        button2_action = QAction(copy_icon,"Copy Row", self)
        button2_action.setCheckable(False)
        self.data_tools.addAction(button2_action)
        button3_action = QAction(paste_icon,"Paste Row", self)
        button3_action.setCheckable(False)
        self.data_tools.addAction(button3_action)
        button4_action = QAction(delete_icon, "Delete Row", self)
        button4_action.setCheckable(False)
        self.data_tools.addAction(button4_action)
        button5_action = QAction(insert_icon, "Insert New Row", self)
        button5_action.setCheckable(False)
        button5_action.triggered.connect(self.add_row)
        self.data_tools.addAction(button5_action)
        self.data_tools.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')

        ### MENU BAR ############################################################
        self.menu_bar.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        file_icon  = QtGui.QIcon.fromTheme("system-file-manager")
        new_icon  = QtGui.QIcon.fromTheme("document-new")
        open_icon  = QtGui.QIcon.fromTheme("document-open")
        save_icon  = QtGui.QIcon.fromTheme("document-save")
        settings_icon  = QtGui.QIcon.fromTheme("preferences-other")
        find_icon  = QtGui.QIcon.fromTheme("edit-find")
        findrepl_icon  = QtGui.QIcon.fromTheme("edit-find-replace")
        about_icon  = QtGui.QIcon.fromTheme("help-about")
        adult_icon  = QtGui.QIcon.fromTheme("/home/brickyard314/.icons/flaticon/professor.png")
        youth_icon  = QtGui.QIcon.fromTheme("/home/brickyard314/.icons/flaticon/cyberpunk.png")
        station_icon = QtGui.QIcon("/home/brickyard314/.icons/flaticon/placeholder.png")
        route_icon = QtGui.QIcon("/home/brickyard314/.icons/flaticon/route.png")
        waypoint_icon =QtGui.QIcon("/home/brickyard314/.icons/flaticon/flag.png")
        faq_icon  = QtGui.QIcon.fromTheme("help-faq")

        file_menu = self.menu_bar.addMenu('&File')

        new_act = file_menu.addAction(new_icon, '&New')
        new_act.setShortcut('Ctrl+N')
        new_act.setStatusTip('Create New Event')
        new_act.triggered.connect(self.new_event)
        file_menu.addAction(new_act)

        open_act = file_menu.addAction(open_icon, '&Open')
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip('Open an Event')
        open_act.triggered.connect(self.open_filename_dialog)
        file_menu.addAction(open_act)

        save_act = file_menu.addAction(save_icon, '&Save')
        save_act.setShortcut('Ctrl+S')
        save_act.setStatusTip('Save Current Event')
        save_act.triggered.connect(self.save_file_dialog)
        file_menu.addAction(save_act)

        export_act = file_menu.addAction('&Export')
        # export_act.triggered.connect(self.export_dialog)
        file_menu.addAction(export_act)

        saveall_act = file_menu.addAction('Save &All')
        file_menu.addAction(saveall_act)

        reload_act = file_menu.addAction('&Reload from disk')
        file_menu.addAction(reload_act)

        settings_act = file_menu.addAction(settings_icon, 'Settings')
        settings_act.setStatusTip('Edit how Derby Runner looks and works')
        # settings_act.triggered.connect(self.settings_dialog)
        file_menu.addAction(settings_act)

        edit_menu = self.menu_bar.addMenu('&Edit')
        cut_act = edit_menu.addAction(cut_icon, 'Cu&t')
        edit_menu.addAction(cut_act)
        copy_act = edit_menu.addAction(copy_icon, '&Copy')
        edit_menu.addAction(copy_act)
        paste_act = edit_menu.addAction(paste_icon, '&Paste')
        edit_menu.addAction(paste_act)
        del_act = edit_menu.addAction(delete_icon, '&Delete')
        edit_menu.addAction(del_act)
        find_act = edit_menu.addAction(find_icon, '&Find')
        edit_menu.addAction(find_act)
        repl_act = edit_menu.addAction(findrepl_icon, '&Replace')
        edit_menu.addAction(repl_act)
        selall_act = edit_menu.addAction('Select &All')
        edit_menu.addAction(selall_act)

        view_menu = self.menu_bar.addMenu('&View')

        adults_act = view_menu.addAction(adult_icon, '&Adults')
        adults_act.setShortcut('Ctrl+A')
        adults_act.setStatusTip('Switch to Adults Table')
        view_menu.addAction(adults_act)
        adults_act.triggered.connect(lambda  : self.change_model('adults'))

        youths_act = view_menu.addAction(youth_icon, '&Youths')
        youths_act.setShortcut('Ctrl+Y')
        youths_act.setStatusTip('Switch to Youths Table')
        view_menu.addAction(youths_act)
        youths_act.triggered.connect(lambda  : self.change_model('youths'))

        waypoints_act = view_menu.addAction(waypoint_icon, '&Waypoints')
        waypoints_act.setShortcut('Ctrl+W')
        waypoints_act.setStatusTip('Switch to Waypoints Table')
        view_menu.addAction(waypoints_act)
        waypoints_act.triggered.connect(lambda : self.change_model('waypoints'))

        stations_act = view_menu.addAction(station_icon, '&Stations')
        stations_act.setShortcut('Ctrl+S')
        stations_act.setStatusTip('Switch to Stations Table')
        view_menu.addAction(stations_act)
        stations_act.triggered.connect(lambda : self.change_model('stations'))

        courses_act = view_menu.addAction('&Courses')
        courses_act.setShortcut('Ctrl+C')
        courses_act.setStatusTip('Switch to Courses Table')
        view_menu.addAction(courses_act)
        courses_act.triggered.connect(lambda : self.change_model('courses'))

        coursepoints_act = view_menu.addAction(route_icon, 'Course &Points')
        coursepoints_act.setShortcut('Ctrl+P')
        coursepoints_act.setStatusTip('Switch to Coursepoints Table')
        view_menu.addAction(coursepoints_act)
        coursepoints_act.triggered.connect(lambda : self.change_model('coursepoints'))

        units_act = view_menu.addAction('&Units')
        units_act.setShortcut('Ctrl+U')
        units_act.setStatusTip('Switch to Units Table')
        view_menu.addAction(units_act)
        units_act.triggered.connect(lambda : self.change_model('units'))

        squads_act = view_menu.addAction('S&quads')
        squads_act.setShortcut('Ctrl+Q')
        squads_act.setStatusTip('Switch to Squads Table')
        view_menu.addAction(squads_act)
        squads_act.triggered.connect(lambda : self.change_model('squads'))

        schedules_act = view_menu.addAction('Sc&hedules')
        schedules_act.setShortcut('Ctrl+H')
        schedules_act.setStatusTip('Switch to Schedules Table')
        view_menu.addAction(schedules_act)
        schedules_act.triggered.connect(lambda : self.change_model('schedules'))

        itineraries_act = view_menu.addAction('&Itineraries')
        itineraries_act.setShortcut('Ctrl+I')
        itineraries_act.setStatusTip('Switch to Itineraries Table')
        view_menu.addAction(itineraries_act)
        itineraries_act.triggered.connect(lambda : self.change_model('itineraries'))

        maps_menu = self.menu_bar.addMenu('&Maps')
        scores_menu = self.menu_bar.addMenu('Scoreboard')
        help_menu = self.menu_bar.addMenu('&Help')
        about_act = help_menu.addAction(about_icon, '&About')
        about_act.setShortcut('Ctrl+A')
        about_act.setStatusTip('About Derby Runner')
        help_menu.addAction(about_act)
#        about_act.triggered.connect(help_about)

        self.menu_bar.adjustSize()
        self.setMenuBar(self.menu_bar)
        # #UTILITIES ##########################
        widget1 = Color('red')
        widget1.setFixedHeight(400)
        widget2 = QtWidgets.QCalendarWidget()

        widget1.setGeometry(QtCore.QRect(0, 0, 400, 800))
        self.splitter_data.setGeometry(QtCore.QRect(5, 9, 600, 600))
        self.data_tools.setGeometry(QtCore.QRect(0, 0, 800, 32))
        self.data_tools.setFixedHeight(55)
        self.data_tools.setIconSize(QSize(50, 50))

        self.splitter_utils.addWidget(widget1)
        self.splitter_utils.addWidget(widget2)
        self.splitter_utils.addWidget(self.mapwidget)
        self.splitter_data.addWidget(self.data_tools)
        self.splitter_data.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(self.layout_main)
        self.setCentralWidget(widget)


        atexit.register(goodbye, data=self.df2)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    t = 250
    l = 350
    w = 2500
    h = 1500
    window.setGeometry(QtCore.QRect(t, l, w, h))
    window.show()
    app.exec_()
