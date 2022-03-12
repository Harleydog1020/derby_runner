import sys
import time
import dr_utils as dru
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QFileDialog, QVBoxLayout, QLabel, QFrame,
    QApplication, QToolBar, QAction, QMenuBar, QSplitter, QProgressBar
)


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


# ##############################################################################
# CLASS Model - To translate data to object that feeds QTableView
# ##############################################################################
class NewModel(QtCore.QAbstractTableModel):
    def __init__(self, data:object) -> object:
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

class Model(QtCore.QAbstractTableModel):
    def __init__(self, table):
        super().__init__()
        self.table = table

    def rowCount(self, parent):
        return len(self.table)

    def columnCount(self, parent):
        return len(self.table[0])

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) :
    #     if role == Qt.DisplayRole and orientation == Qt.Horizontal:
    #         return self.head_labels[section]

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.table[index.row()][index.column()]

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            print("A change! " + str(value))
            self.table[index.row()][index.column()] = value
            print(self.table)
        return True


# ##############################################################################
# CLASS CustomTableDelegate
#
# ##############################################################################

class CustomTableDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CustomTableDelegate, self).__init__(parent)
        # self.setMouseTracking(True)

        self._mousePressAnchor = ''
        self._lastHoveredAnchor = ''

    def paint(self, painter, option, index):
        if option.state & QtWidgets.QStyle.State_MouseOver:
            painter.fillRect(option.rect, QtGui.QColor(0, 100, 200))
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
        else:
            painter.fillRect(option.rect, QtGui.QColor(150, 220, 255))
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def mouse_press_event(self, event):
        anchor = self.anchor_at(event.pos())
        self._mousePressAnchor = anchor

    def mouse_move_event(self, event):
        anchor = self.anchor_at(event.pos())
        if self._mousePressAnchor != anchor:
            self._mousePressAnchor = ''

        if self._lastHoveredAnchor != anchor:
            self._lastHoveredAnchor = anchor
            if self._lastHoveredAnchor:
                QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            else:
                QtWidgets.QApplication.restoreOverrideCursor()

    def mouse_release_event(self, event):
        if self._mousePressAnchor:
            anchor = self.anchor_at(event.pos())
            if anchor == self._mousePressAnchor:
                self.link_activated.emit(anchor)
            self._mousePressAnchor = ''

    def anchor_at(self, pos):
        index = self.indexAt(pos)
        if index.isValid():
            delegate = self.itemDelegate(index)
            if delegate:
                item_rect = self.visualRect(index)
                relative_click_position = pos - item_rect.topLeft()
                html = self.model().data(index, QtCore.Qt.DisplayRole)
                return delegate.anchor_at(html, relative_click_position)
        return ''


class CustomTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(CustomTableView, self).__init__(parent)

    def set_mouse_over(self, row):
        print(row)


def read_stylesheets():
    ssh_file = "/home/brickyard314/PycharmProjects/derby_runner/derby_runner/style_blue.css"
    with open(ssh_file, "r") as fh:
        style_blue = fh.read()

    ssh_file = "/home/brickyard314/PycharmProjects/derby_runner/derby_runner/style_black.css"
    with open(ssh_file, "r") as fh:
        style_black = fh.read()

    ssh_file = "/home/brickyard314/PycharmProjects/derby_runner/derby_runner/style_gray.css"
    with open(ssh_file, "r") as fh:
        style_gray = fh.read()

    style_sheet = style_blue
    return style_sheet


class StyleDriver:
    def __init__(self):
        super(StyleDriver, self).__init__()


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 350)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.counter = 0
        self.n = 100
        self.init_splash()
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def init_splash(self):
        # layout to display splash scrren frame
        layout = QVBoxLayout()
        self.setLayout(layout)
        # splash screen frame
        self.frame = QFrame()
        layout.addWidget(self.frame)
        # splash screen title
        self.title_label = QLabel(self.frame)
        self.title_label.setObjectName('title_label')
        self.title_label.resize(690, 120)
        self.title_label.move(0, 5)  # x, y
        self.title_label.setText('Loading Derby Runner')
        self.title_label.setAlignment(Qt.AlignCenter)
        # splash screen title description
        self.description_label = QLabel(self.frame)
        self.description_label.resize(690, 40)
        self.description_label.move(0, self.title_label.height())
        self.description_label.setObjectName('desc_label')
        self.description_label.setText('<b>Derby Runner</b>')
        self.description_label.setAlignment(Qt.AlignCenter)
        # splash screen pogressbar
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, 180)  # self.description_label.y()+130
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)
        # spash screen loading label
        self.loading_label = QLabel(self.frame)
        self.loading_label.resize(self.width() - 10, 50)
        self.loading_label.move(0, self.progressBar.y() + 70)
        self.loading_label.setObjectName('loading_label')
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setText('Loading...')

    def loading(self):
        # set progressbar value
        self.progressBar.setValue(self.counter)
        # stop progress if counter
        # is greater than n and
        # display main window app
        if self.counter >= self.n:
            self.timer.stop()
            self.close()
            time.sleep(1)
            self.WindowApp = WindowApp()
            self.WindowApp.show()
        self.counter += 1


class WindowApp(QtWidgets.QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Derby Runner v0.1")
        self.setGeometry(1000, 600, 1750, 500)
        self.setText("Derby Runner v0.1")
        self.setInformativeText("Copyright ©2022")
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setDetailedText("More to come...")
        self.show()


class DateEditDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, widget, option, index):
        editor = QtWidgets.QDateEdit(widget)
        editor.setMinimumHeight(50)
        editor.setStyleSheet("background-color: red;")
        if option.state & QtWidgets.QStyle.State_MouseOver:
            editor.setStyleSheet("background-color: green; color: yellow;")
        else:
            editor.setStyleSheet("background-color: yellow; color: green;")
        return editor


class LabelEditDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, widget, option, index):
        editor = QtWidgets.QLabel(widget)
        return editor


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
        value = index.data(QtCore.Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, QtCore.Qt.DisplayRole, QtCore.QVariant(value))

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ComboBoxDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = None

    def set_items(self, items):
        self.items = items

    def createEditor(self, widget, option, index):
        editor = QtWidgets.QComboBox(widget)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        editor.setCurrentIndex(0)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex(), QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        text = self.items[index.row()]
        option.text = text
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_ItemViewItem, option, painter)


def help_about():
    about_msg = QtWidgets.QMessageBox()
    about_msg.setStyleSheet("font-size: 10pt;")
    about_msg.setWindowTitle("About Derby Runner")
    about_msg.setText("Derby Runner v0.1")
    about_msg.setInformativeText("Copyright ©2022")
    about_msg.setIcon(QtWidgets.QMessageBox.Information)
    about_msg.setDetailedText("More to come...")
    about_msg.exec_()


def find_screen(self):
    find_screen = QtWidgets.QApplication(sys.argv)
    screen = find_screen.primaryScreen()
    size = screen.size()
    rect = screen.availableGeometry()
    screen_width = rect.width()
    screen_height = rect.height()
    self.top = int(0.25 * screen_height)
    self.left = int(0.25 * screen_width)
    self.height = int(0.5 * screen_height)
    self.width = int(0.5 * screen_width)

    print('Screen: %s' % screen.name())
    print('Size: %d x %d' % (size.width(), size.height()))
    print('Available: %d x %d' % (rect.width(), rect.height()))
    return


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        dru.init_lists(self)
        self.new_event()
        self.current_table = 'units'

        self.layout = QtWidgets.QVBoxLayout()
        self.comboBox = QtWidgets.QComboBox()
        self.setWindowTitle("Derby Runner")

        # find_screen(self)
        t = 250
        l = 350
        w = 2500
        h = 1500
        self.setGeometry(l, t, w, h)

        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("central_widget")
        self.menu_bar = QMenuBar()
        self.menu_bar.setStyleSheet("font-size: 12pt; padding: 5px; margin: 1px;")
        self.menu_bar.setObjectName("menu_bar")
        self.setMenuBar(self.menu_bar)
        # # LAYOUTS ############################################################
        self.layout_main = QHBoxLayout()
        self.splitter_main = QSplitter(Qt.Horizontal)
        self.splitter_data = QSplitter(Qt.Vertical)
        self.splitter_utils = QSplitter(Qt.Vertical)
        self.splitter_data.setGeometry(QtCore.QRect(5, 9, 2200, 1100))
        # # TABLE VIEW #########################################################
        # self.table_view = CustomTableView()
        self.table_view = QtWidgets.QTableView()
        # create table data:
        self.table = self.setup_table(self.df_units)
        self.model = Model(self.table)
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.model)

        date_delegate = DateEditDelegate(self)
        label_delegate = LabelEditDelegate(self)
        combo_delegate = ComboBoxDelegate(self)

        if self.current_table == 'units':
            choices = ['Crew', 'Pack', 'Post', 'Ship', 'Troop', 'Other']
            self.table_view.setItemDelegateForColumn(0, Delegate(self, choices))
            for row in range(len(self.table)):
                self.table_view.openPersistentEditor(self.model.index(row, 0))
        print(self.table)
        self.setup_ui()

    def setup_ui(self):
        self.new_event()
        current_style = read_stylesheets()

        h_lw = QtWidgets.QWidget(self.central_widget)
        t = 250
        l = 350
        w = 2500
        h = 1500
        h_lw.setGeometry(QtCore.QRect(t, l, w, h))
        # MENU BAR ##############################################################

        file_menu = self.menu_bar.addMenu('&File')

        new_act = file_menu.addAction('&New')
        new_act.setShortcut('Ctrl+N')
        new_act.setStatusTip('Create New Event')
        new_act.triggered.connect(self.new_event)
        file_menu.addAction(new_act)

        open_act = file_menu.addAction('&Open')
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip('Open an Event')
        open_act.triggered.connect(self.open_filename_dialog)
        file_menu.addAction(open_act)

        save_act = file_menu.addAction('&Save')
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

        settings_act = file_menu.addAction('Settings')
        settings_act.setStatusTip('Edit how Derby Runner looks and works')
        # settings_act.triggered.connect(self.settings_dialog)
        file_menu.addAction(settings_act)

        edit_menu = self.menu_bar.addMenu('&Edit')
        cut_act = edit_menu.addAction('Cu&t')
        edit_menu.addAction(cut_act)
        copy_act = edit_menu.addAction('&Copy')
        edit_menu.addAction(copy_act)
        paste_act = edit_menu.addAction('&Paste')
        edit_menu.addAction(paste_act)
        del_act = edit_menu.addAction('&Delete')
        edit_menu.addAction(del_act)
        find_act = edit_menu.addAction('&Find')
        edit_menu.addAction(find_act)
        repl_act = edit_menu.addAction('&Replace')
        edit_menu.addAction(repl_act)
        selall_act = edit_menu.addAction('Select &All')
        edit_menu.addAction(selall_act)

        view_menu = self.menu_bar.addMenu('&View')

        waypoints_act = view_menu.addAction('&Waypoints')
        waypoints_act.setShortcut('Ctrl+W')
        waypoints_act.setStatusTip('Switch to Waypoints Table')
        view_menu.addAction(waypoints_act)
        waypoints_act.triggered.connect(self.view_waypoints)

        stations_act = view_menu.addAction('&Stations')
        stations_act.setShortcut('Ctrl+S')
        stations_act.setStatusTip('Switch to Stations Table')
        view_menu.addAction(stations_act)
        stations_act.triggered.connect(self.view_stations)

        courses_act = view_menu.addAction('&Courses')
        courses_act.setShortcut('Ctrl+C')
        courses_act.setStatusTip('Switch to Courses Table')
        view_menu.addAction(courses_act)
        courses_act.triggered.connect(self.view_courses)

        coursepoints_act = view_menu.addAction('Course &Points')
        coursepoints_act.setShortcut('Ctrl+P')
        coursepoints_act.setStatusTip('Switch to Coursepoints Table')
        view_menu.addAction(coursepoints_act)
        coursepoints_act.triggered.connect(self.view_coursepoints)

        units_act = view_menu.addAction('&Units')
        units_act.setShortcut('Ctrl+U')
        units_act.setStatusTip('Switch to Units Table')
        view_menu.addAction(units_act)
        units_act.triggered.connect(self.view_units)

        squads_act = view_menu.addAction('S&quads')
        squads_act.setShortcut('Ctrl+Q')
        squads_act.setStatusTip('Switch to Squads Table')
        view_menu.addAction(squads_act)
        squads_act.triggered.connect(self.view_squads)

        schedules_act = view_menu.addAction('Sc&hedules')
        schedules_act.setShortcut('Ctrl+H')
        schedules_act.setStatusTip('Switch to Schedules Table')
        view_menu.addAction(schedules_act)
        schedules_act.triggered.connect(self.view_schedules)

        itineraries_act = view_menu.addAction('&Itineraries')
        itineraries_act.setShortcut('Ctrl+I')
        itineraries_act.setStatusTip('Switch to Itineraries Table')
        view_menu.addAction(itineraries_act)
        itineraries_act.triggered.connect(self.view_itineraries)

        maps_menu = self.menu_bar.addMenu('&Maps')
        help_menu = self.menu_bar.addMenu('&Help')
        about_act = help_menu.addAction('&About')
        about_act.setShortcut('Ctrl+A')
        about_act.setStatusTip('About Derby Runner')
        help_menu.addAction(about_act)
        about_act.triggered.connect(help_about)

        # #TOOL BAR ########################################################################
        data_tools = QToolBar()
        data_tools.setGeometry(QtCore.QRect(0, 0, 800, 32))
        data_tools.setFixedHeight(45)
        data_tools.setIconSize(QSize(32, 32))
        self.splitter_data.addWidget(data_tools)

        button1_action = QAction(
            QIcon("/home/brickyard314/PycharmProjects/derby_runner/resources/bonus/icons-32/blue-document.png"),
            "Your button",
            self)
        button1_action.setStatusTip("This is not your button")
        button1_action.setCheckable(True)
        data_tools.addAction(button1_action)
        self.splitter_data.addWidget(data_tools)

        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(False)
        vertical_header = self.table_view.verticalHeader()
        vertical_header.hide()
        self.splitter_data.addWidget(self.table_view)

        # #UTILITIES ##########################
        widget1 = Color('red')
        self.splitter_utils.addWidget(widget1)
        widget2 = QtWidgets.QCalendarWidget(h_lw)
        widget2.setStyleSheet(
            'font-size: 11pt; color: "black"; border: 1px solid #5CACEE; selection-background-color: #1B89CA; '
            'selection-color: #F0F0F0;')
        self.splitter_utils.addWidget(widget2)
        web_widget = QWebEngineView()
        with open('/home/brickyard314/NC_maps/nc_test.html', 'r') as f:
            html = f.read()
        web_widget.setHtml(html)
        web_widget.setStyleSheet(current_style)
        self.splitter_utils.addWidget(web_widget)

        # MAIN WINDOW ##################################################################
        self.layout_main.setContentsMargins(5, 5, 5, 5)
        self.layout_main.setSpacing(20)
        self.splitter_main.addWidget(self.splitter_data)
        self.splitter_main.addWidget(self.splitter_utils)
        self.layout_main.addWidget(self.splitter_main)

        widget = QWidget()
        widget.setLayout(self.layout_main)
        self.setCentralWidget(widget)
        print(self.model)
        # self.setup_table(self.df_units)

    def setup_table(self, data):
        table = []
        i = 0
        for index, row in data.iterrows():
            table.append(data.iloc[i].to_list())
            i = i + 1
        return table

    def old_setup_table(self, data):
        choices = ['Crew', 'Pack', 'Post', 'Ship', 'Troop', 'Other']

        # table.append(self.df_units.iloc[0].to_list())
        # table.append(self.df_units.iloc[1].to_list())
        column_labels = list(data)
        self.model.setHorizontalHeaderLabels(column_labels)

        i = 0
        for index, row in data.iterrows():
            j = 0
            for col in row:
                item = str(col)
                if item == 'nan':
                    item = ' '
                self.model.setItem(i, j, QtGui.QStandardItem(item))
                j = j + 1
            i = i + 1
        return

    def settings_dialog(self):
        dlg = QtWidgets.QDialog()
        self.layout.addWidget(self.comboBox)
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
        dlg.setLayout(self.layout)
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
        file_name = file_name + ".h5"
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

    def open_filename_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        x = QFileDialog()
        file_name, _ = x.getOpenFileName(caption="Caption", filter="H5F Files (*.h5);;All Files (*)",
                                         options=options)
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

            self.view_waypoints()

    def view_stations(self):
        self.setup_table(self.df_stations)
        return

    def view_waypoints(self):
        self.setup_table(self.df_waypoints)
        return

    def view_courses(self):
        self.setup_table(self.df_courses)
        return

    def view_coursepoints(self):
        self.setup_table(self.df_coursepoints)
        return

    def view_units(self):
        self.setup_table(self.df_units)
        return

    def view_squads(self):
        self.setup_table(self.df_squads)
        return

    def view_adults(self):
        self.setup_table(self.df_adults)
        return

    def view_youths(self):
        self.setup_table(self.df_youths)
        return

    def view_schedules(self):
        self.setup_table(self.df_schedules)
        return

    def view_itineraries(self):
        self.setup_table(self.df_itineraries)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # splash = SplashScreen()
    # splash.show()
    app.exec()
    print("and the answer is")
    print(window.table)
