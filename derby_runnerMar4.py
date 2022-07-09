import atexit
import sys
from os.path import exists

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import dr_utils as dru
import points_editor as pe


# ############################################################################
class PlotCanvas(FigureCanvas):
    """
    A class to handle plotting stations, waypoints and courses for Derby Runner

    Attributes
    ----------
    :fig: matplotlib Figure
        fig acts as the overall driver, holding the .png image and also plotting
        the stations, waypoints and courses

    Methods
    -------
    plot(self):
        description        .
    """

    def __init__(self, parent=None, cnv_width=6, cnv_height=4, dpi=100):
        # fig = Figure(figsize=(cnv_width, cnv_height), dpi=dpi)
        fig, ax = plt.subplots()

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
# CLASS Color - test widget that acts as a placeholder in layouts to facilitate
#               design, development and testing, but ultimately is not meant for
#               actual "production" version
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
    """
    NewModel is meant to take a pandas DataFrame and be the mechanism whereby
    that DataFrame can be presented to the user via the QTableView widget.

    Attributes
    ----------
    data : pandas DataFrame
        This takes any of the various pandas dataframes that hold the
        Derby Runner data and then allows for generic processing of
        those data frames.  It is introduced in a "hint", data: pd.DataFrame,
        so that NewModel code can leverage pandas DataFrame functions and methods
        without being flagged as a warning for being applied to an object which
        is what it would be treated as otherwise.

    Methods
    -------
    flags(self):
        description
    data(self, index, role):
    setData(self, index, value, role=Qt.DisplayRole, **kwargs):
    rowCount(self, index=QtCore.QModelIndex()) -> int:
    columnCount(self, index=QtCore.QModelIndex()) -> int:
    headerData(self, section, orientation, role=Qt.DisplayRole):
    """

    data: pd.DataFrame

    def __init__(self, data: pd.DataFrame):
        super(NewModel, self).__init__()
        self.data = data

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole and role != Qt.EditRole:
            return
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
    """
    Delegate is used in conjunction with NewModel and QTableView to facilitate
    more complicated editing functions such as combo boxes, input data masks
    and data checking.

    Attributes
    ----------
    :choices: list of elements to be used in the combo box
    :self.editor: QtWidgets.QComboBox
        This takes .

    Methods
    -------
    createEditor(self, parent, option, index):
        description
    paint(self, painter, option, index):
    setEditorData(self, editor, index):
    setModelData(self, editor, model, index):
    updateEditorGeometry(self, editor, option, index):
    """

    def __init__(self, owner, choices):
        super().__init__(owner)
        self.editor = QComboBox()
        self.items = choices

    def createEditor(self, parent, option, index):
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


# ##############################################################################
class PlainTextEditDelegate(QtWidgets.QItemDelegate):
    """
       PlainTextEditDelegate is used in conjunction with NewModel and QTableView to
       for fields that would require a simple text editing function.

       Attributes
       ----------
       :self.editor: QtWidgets.QPlainTextEdit()
           This takes .

       Methods
       -------
       createEditor(self, parent, option, index):
           description
       paint(self, painter, option, index):
       """

    def __init__(self, owner):
        super().__init__(owner)
        self.editor = QtWidgets.QPlainTextEdit()

    def createEditor(self, parent, option, index):
        return self.editor

    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QPlainTextEdit()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)


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

        self.df_stations = None
        self.df_settings: pd.DataFrame
        self.df_adults: pd.DataFrame
        self.df_coursepoints: pd.DataFrame
        self.df_courses: pd.DataFrame
        self.df_itineraries: pd.DataFrame
        self.df_schedules: pd.DataFrame
        self.df_stations: pd.DataFrame
        self.df_squads: pd.DataFrame
        self.df_units: pd.DataFrame
        self.df_waypoints: pd.DataFrame
        self.df_youths: pd.DataFrame
        self.df_eveentoptions: pd.DataFrame
        self.df_settings: pd.DataFrame
        # self.map_widget = PlotCanvas(self)

        # self.points_editor = pe.PointEditor(self)

        self.image = Image.open(str('/home/brickyard314/PycharmProjects/drv/resources/woodlake.png'), 'r')

        # ax = self.map_widget.figure.add_subplot(111)
        # ax.set_xticks([-85.785, -85.780, -85.775, -85.770, -85.760])
        # ax.set_yticks([41.856, 41.858, 41.860, 41.862])
        # ax.imshow(self.image, extent=[-85.78590, -85.76597, 41.85403, 41.86310])
        dru.init_lists(self)
        self.new_event()
        self.drsettings = './resources/drsettings.h5'
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

        self.layout_main.setContentsMargins(5, 5, 5, 5)
        self.layout_main.setSpacing(20)
        self.splitter_main.addWidget(self.splitter_data)
        self.splitter_main.addWidget(self.splitter_utils)
        self.layout_main.addWidget(self.splitter_main)
        self.setup_ui()

    def goodbye(self):
        """
        A simple function used to trap EXIT to prompt for save changes
        :param :
        :return:
        """

        dlg = QDialog()
        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlg.button_box = QDialogButtonBox(q_btn)
        dlg.layout = QFormLayout()
        message = QLabel("Would you like to save changes first?")
        message.setAlignment(QtCore.Qt.AlignLeft)
        dlg.layout.addRow(message)

        dlg.button_box.accepted.connect(self.save_file_dialog)
        dlg.button_box.rejected.connect(dlg.reject)
        dlg.layout.addWidget(dlg.button_box)
        dlg.setLayout(dlg.layout)
        dlg.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        dlg.setGeometry(1200, 1200, 800, 600)
        dlg.exec()
        print('Goodbye')
        dlg.close()

    # ##############################################################################
    def refresh_map(self):
        # Need a button added to the tool bar that calls this function
        file_name = self.df_eveentoptions.loc[0, 'map_open']
        self.image = Image.open(file_name, 'r')
        ax = self.map_widget.figure.add_subplot(111)
        image_width = self.image.width
        image_height = self.image.height

        # Get map coordinates
        north = self.df_eveentoptions.loc[0, 'north']
        south = self.df_eveentoptions.loc[0, 'south']
        east = self.df_eveentoptions.loc[0, 'east']
        west = self.df_eveentoptions.loc[0, 'west']
        dist_ns = north - south
        dist_ew = east - west
        ax.imshow(self.image, extent=[west, east, south, north])

        # Calculate X & Y tick labels
        x_ticks = [(west + (0.20 * dist_ew)), (west + (0.40 * dist_ew)), (west + (0.60 * dist_ew)),
                   (west + (0.80 * dist_ew))]
        y_ticks = [(south + (0.20 * dist_ns)), (south + (0.40 * dist_ns)), (south + (0.60 * dist_ns)),
                   (south + (0.80 * dist_ns))]
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)

        # Get Station coordinates then plot
        stations_x = np.array(self.df_stations['Longitude'])
        stations_y = np.array(self.df_stations['Latitude'])
        ax.plot(stations_x, stations_y, "o")

        # Get Waypoint coordinates then plot
        waypoints_x = np.array(self.df_waypoints['Longitude'])
        waypoints_y = np.array(self.df_waypoints['Latitude'])
        ax.plot(waypoints_x, waypoints_y, "*")

        # Get coursepoints and plot course lines
        return

    def show_data(self):
        """Used for development and testing"""
        print("show_data: ")
        print(self.df2)

    def settings_dialog(self):
        def getinfo():
            self.df_settings.loc[0, 'file_onopen'] = dlg.file_name.text()
            self.df_settings.loc[0, 'file_directory'] = dlg.dir_name.text()
            print(self.df_settings)
            dlg.close()

        dlg = QDialog()
        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlg.button_box = QDialogButtonBox(q_btn)
        dlg.layout = QFormLayout()
        message = QLabel("Hi there.")
        message.setAlignment(QtCore.Qt.AlignLeft)
        dlg.layout.addRow(message)

        file_str = self.df_settings.loc[0, 'file_onopen']
        if len(file_str) == 0: 
            file_str = ' '
        dlg.file_name = QLineEdit(file_str)
        dlg.layout.addRow(QLabel("File to use at open: "), dlg.file_name)

        dir_str = self.df_settings.loc[0, 'file_directory']
        if len(file_str) == 0: 
            dir_str = ' '
        dlg.dir_name = QLineEdit(dir_str)
        dlg.layout.addRow(QLabel("Derby Runner directory: "), dlg.dir_name)
        dlg.button_box.accepted.connect(getinfo)
        dlg.button_box.rejected.connect(dlg.reject)
        dlg.layout.addWidget(dlg.button_box)
        dlg.setLayout(dlg.layout)
        dlg.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        dlg.setGeometry(1200, 1200, 800, 600)
        dlg.exec()

    def add_row(self):
        rows = sorted(set(index.row() for index in
                          self.table.selectedIndexes()))

        if self.current_table == 'stations':
            df_columns = self.stations_columns
        elif self.current_table == 'waypoints':
            df_columns = self.waypoints_columns
        elif self.current_table == 'units':
            df_columns = self.units_columns
        elif self.current_table == 'squads':
            df_columns = self.squads_columns
        elif self.current_table == 'coursepoints':
            df_columns = self.coursepoint_columns
        elif self.current_table == 'itineraries':
            df_columns = self.itinerary_columns
        elif self.current_table == 'schedules':
            df_columns = self.schedules_columns
        elif self.current_table == 'youths':
            df_columns = self.youths_columns
        elif self.current_table == 'adults':
            df_columns = self.adults_columns
        elif self.current_table == 'courses':
            df_columns = self.courses_columns
        else:
            print("Unknown error #1 in ADD_ROW function")

        # if no rows selected, add one row to the end
        if len(rows) == 0:
            new_row = pd.DataFrame(columns=df_columns, index=[0])
            new_row.fillna('  ', inplace=True)
        else:
            new_row = pd.DataFrame(columns=df_columns, index=range(len(rows)))
            new_row.fillna('  ', inplace=True)

        if self.current_table == 'stations':
            self.df_stations = self.df_stations.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_stations)
        elif self.current_table == 'waypoints':
            self.df_waypoints = self.df_waypoints.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_waypoints)
        elif self.current_table == 'units':
            self.df_units = self.df_units.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_units)
        elif self.current_table == 'squads':
            self.df_squads = self.df_squads.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_squads)
        elif self.current_table == 'coursepoints':
            self.df_coursepoints = self.df_coursepoints.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_coursepoints)
        elif self.current_table == 'itineraries':
            self.df_itineraries = self.df_itineraries.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_itineraries)
        elif self.current_table == 'schedules':
            self.df_schedules = self.df_schedules.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_schedules)
        elif self.current_table == 'youths':
            self.df_youths = self.df_youths.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_youths)
        elif self.current_table == 'adults':
            self.df_adults = self.df_adults.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_adults)
        elif self.current_table == 'courses':
            self.df_courses = self.df_courses.append(new_row, ignore_index=True)
            self.model = NewModel(self.df_courses)
        else:
            print("Unknown error #2 in ADD_ROW function")

        self.table.setModel(self.model)

    def del_row(self):
        rows = sorted(set(index.row() for index in
                          self.table.selectedIndexes()))
        print(len(rows))
        for row in rows:
            print('Row %d is selected' % row)

        # if no rows selected, popup "no rows selected"
        # if 1 or more selected, delete rows selected

    def copy_row(self):
        rows = sorted(set(index.row() for index in
                          self.table.selectedIndexes()))
        print(len(rows))
        for row in rows:
            print('Row %d is selected' % row)

        # if no rows selected, popup "no rows selected"
        # if 1 or more selected, copy to temp DF then add below last row

    def new_event(self):
        self.df_settings = dru.init_settings(self)
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
        self.df_eveentoptions = dru.init_eventoptions(self)

    def quick_save(self):
        file_name = self.current_filename
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
        self.df_eveentoptions.to_hdf(file_name, key='options', mode='a')
        self.df_settings.to_hdf(self.drsettings, key='settings', mode='a')

    def save_file_dialog(self):
        x = QFileDialog()
        x.setGeometry(500, 500, 1000, 1500)
        file_name, _ = x.getSaveFileName(caption="Caption", directory="/home/brickyard314/DerbyRunner",
                                         filter="H5F Files (*.h5);;All Files (*)")
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
            self.df_eveentoptions.to_hdf(file_name, key='options', mode='a')
        self.df_settings.to_hdf(self.drsettings, key='settings', mode='a')
        self.current_filename = file_name
        print(self.df_eveentoptions)
        return

    def open_filename_dialog(self):
        x = QFileDialog()
        x.setGeometry(500, 500, 1000, 1500)
        self.df_eveentoptions: pd.DataFrame
        file_name, _ = x.getOpenFileName(caption="Open Derby Runner files", directory="/home/brickyard314/DerbyRunner",
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
            self.df_eveentoptions = pd.read_hdf(file_name, key='options', mode='r')
            self.df_settings = pd.read_hdf(self.drsettings, key='settings', mode='r')
            self.change_model('units')
            map_name = self.df_eveentoptions.loc[0, 'map_open']
            print("Map: " + map_name)
            self.image = Image.open(str('/home/brickyard314/DerbyRunner/map.png'), 'r')
            self.table.resizeColumnsToContents()
        self.current_filename = file_name
        return

    def import_map_dialog(self):
        # for reference, get maps from https://www.openstreetmap.org/
        # for instructions https://towardsdatascience.com/simple-gps-data-visualization-using-python-and-open-street-maps-50f992e9b676

        x = QFileDialog()
        x.setGeometry(500, 500, 1000, 1500)

        file_name, _ = x.getOpenFileName(caption="Open image files",
                                         filter="Image Files (*.png);;All Files (*)")
        if file_name:
            self.image = Image.open(file_name, 'r')
            image_width = self.image.width
            image_height = self.image.height
            self.df_eveentoptions.loc[0, 'map_open'] = file_name
            ax = self.map_widget.figure.add_subplot(111)
            ax.set_xticks([0, 20, 40, 60, 80, 100])
            ax.set_yticks([0, 20, 40, 60, 80, 100])
            ax.imshow(self.image, extent=[0, 100, 0, 100])
        return

    def map_settings(self):
        def get_mapinfo():
            self.df_eveentoptions.loc[0, 'north'] = dlg.north.text()
            self.df_eveentoptions.loc[0, 'south'] = dlg.south.text()
            self.df_eveentoptions.loc[0, 'east'] = dlg.east.text()
            self.df_eveentoptions.loc[0, 'west'] = dlg.west.text()
            dlg.close()

        dlg = QDialog()
        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlg.button_box = QDialogButtonBox(q_btn)
        dlg.layout = QFormLayout()
        message = QLabel("Enter Map Boundary Coordinates.")
        message.setAlignment(QtCore.Qt.AlignLeft)
        dlg.layout.addRow(message)

        dlg.north = QLineEdit()
        dlg.north.setValidator(QDoubleValidator(-180.99999, 180.99999, 6))
        dlg.layout.addRow(QLabel("North Latitude: "), dlg.north)

        dlg.south = QLineEdit()
        dlg.south.setValidator(QDoubleValidator(-180.99999, 180.99999, 6))
        dlg.layout.addRow(QLabel("South Latitude: "), dlg.south)

        dlg.east = QLineEdit()
        dlg.east.setValidator(QDoubleValidator(-180.99999, 180.99999, 6))
        dlg.layout.addRow(QLabel("East Longitude: "), dlg.east)

        dlg.west = QLineEdit()
        dlg.west.setValidator(QDoubleValidator(-180.99999, 180.99999, 6))
        dlg.layout.addRow(QLabel("West Longitude: "), dlg.west)

        dlg.button_box.accepted.connect(get_mapinfo)
        dlg.button_box.rejected.connect(dlg.reject)
        dlg.layout.addWidget(dlg.button_box)
        dlg.setLayout(dlg.layout)
        dlg.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        dlg.setGeometry(1200, 1200, 800, 600)
        dlg.exec()

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

    # SETUP UI #################################################################
    def setup_ui(self):
        """Assembles all the pieces for the Main Window"""

        self.df_settings = pd.read_hdf(self.drsettings, key='settings', mode='r')
        dir_str = self.df_settings.loc[0, 'file_directory']
        file_str = self.df_settings.loc[0, 'file_onopen']
        file_name = dir_str.strip() + file_str.strip()
        if exists(file_name):
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
            self.df_eveentoptions = pd.read_hdf(file_name, key='options', mode='r')
            self.df_settings = pd.read_hdf(self.drsettings, key='settings', mode='r')
            self.change_model('units')
            map_name = self.df_eveentoptions.loc[0, 'map_open']
            self.image = Image.open(str(map_name), 'r')

            # ax = self.map_widget.figure.add_subplot(111)
            # ax.set_xticks([-85.785, -85.780, -85.775, -85.770, -85.760])
            # ax.set_yticks([41.856, 41.858, 41.860, 41.862])
            # ax.imshow(self.image, extent=[-85.78590, -85.76597, 41.85403, 41.86310])
            self.table.resizeColumnsToContents()
            self.current_filename = file_name

        else:
            print("Nope.  Can't find it." + file_name)

        data2 = [['10', 'Alex'], ['12', 'Bob'], ['13', 'Clarke']]
        self.df2 = pd.DataFrame(data2, columns=['Age', 'Name'])

        if self.current_table == 'adults':
            print("Adults")
        elif self.current_table == 'units':
            choices = self.unit_types
            self.model = NewModel(self.df_units)
        else:
            choices = ['Alex', 'Bob', 'Clarke', 'Ship', 'Troop', 'Other']
            self.model = NewModel(self.df2)

        self.table.setModel(self.model)

        # TOOL BAR ############################################################
        # Qt themes work on all platforms, it's just that on Linux you get the theme for free.
        # On non-Linux platforms you have to define your own icon theme from scratch.
        # However, this is only really worth doing if you want to have a Linux-native look,
        # for other use cases the QResource system is simpler.

        cut_icon = QtGui.QIcon.fromTheme("edit-cut")
        copy_icon = QtGui.QIcon.fromTheme("edit-copy")
        paste_icon = QtGui.QIcon.fromTheme("edit-paste")
        delete_icon = QtGui.QIcon.fromTheme("edit-delete")
        insert_icon = QtGui.QIcon.fromTheme("list-add")
        # Select Row .../table-select-row
        # import_icon = QtGui.QIcon.fromTheme("")
        # Export ".../document-export.png
        icon = QtGui.QIcon.fromTheme("document-new")
        button1_action = QAction(cut_icon, "Cut Row", self)
        button1_action.setCheckable(False)

        self.data_tools.addAction(button1_action)
        button2_action = QAction(copy_icon, "Copy Row", self)
        button2_action.setCheckable(False)
        self.data_tools.addAction(button2_action)
        button3_action = QAction(paste_icon, "Paste Row", self)
        button3_action.setCheckable(False)
        self.data_tools.addAction(button3_action)
        button4_action = QAction(delete_icon, "Delete Row", self)
        button4_action.setCheckable(False)
        button4_action.triggered.connect(self.del_row)
        self.data_tools.addAction(button4_action)
        button5_action = QAction(insert_icon, "Insert New Row", self)
        button5_action.setCheckable(False)
        button5_action.triggered.connect(self.add_row)
        self.data_tools.addAction(button5_action)
        self.data_tools.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')

        button6_action = QAction(icon, "Refresh Map", self)
        button6_action.setCheckable(False)
        button6_action.triggered.connect(self.refresh_map)
        self.data_tools.addAction(button6_action)

        # MENU BAR ############################################################
        self.menu_bar.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        file_icon = QtGui.QIcon.fromTheme("system-file-manager")
        new_icon = QtGui.QIcon.fromTheme("document-new")
        open_icon = QtGui.QIcon.fromTheme("document-open")
        save_icon = QtGui.QIcon.fromTheme("document-save")
        settings_icon = QtGui.QIcon.fromTheme("preferences-other")
        find_icon = QtGui.QIcon.fromTheme("edit-find")
        findrepl_icon = QtGui.QIcon.fromTheme("edit-find-replace")
        about_icon = QtGui.QIcon.fromTheme("help-about")
        adult_icon = QtGui.QIcon.fromTheme("/home/brickyard314/.icons/flaticon/professor.png")
        youth_icon = QtGui.QIcon.fromTheme("/home/brickyard314/.icons/flaticon/cyberpunk.png")
        station_icon = QtGui.QIcon("/home/brickyard314/.icons/flaticon/placeholder.png")
        route_icon = QtGui.QIcon("/home/brickyard314/.icons/flaticon/route.png")
        waypoint_icon = QtGui.QIcon("/home/brickyard314/.icons/flaticon/flag.png")
        faq_icon = QtGui.QIcon.fromTheme("help-faq")

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
        # save_act.triggered.connect(self.save_file_dialog)
        file_menu.addAction(save_act)

        saveas_act = file_menu.addAction(save_icon, 'Save &As')
        saveas_act.setShortcut('Ctrl+A')
        saveas_act.setStatusTip('Save Current Event')
        saveas_act.triggered.connect(self.save_file_dialog)
        file_menu.addAction(saveas_act)

        export_act = file_menu.addAction('&Export')
        # export_act.triggered.connect(self.export_dialog)
        file_menu.addAction(export_act)

        saveall_act = file_menu.addAction('Save &All')
        file_menu.addAction(saveall_act)

        reload_act = file_menu.addAction('&Reload from disk')
        file_menu.addAction(reload_act)

        settings_act = file_menu.addAction(settings_icon, 'Settings')
        settings_act.setStatusTip('Edit how Derby Runner looks and works')
        settings_act.triggered.connect(self.settings_dialog)
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
        adults_act.triggered.connect(lambda: self.change_model('adults'))

        youths_act = view_menu.addAction(youth_icon, '&Youths')
        youths_act.setShortcut('Ctrl+Y')
        youths_act.setStatusTip('Switch to Youths Table')
        view_menu.addAction(youths_act)
        youths_act.triggered.connect(lambda: self.change_model('youths'))

        waypoints_act = view_menu.addAction(waypoint_icon, '&Waypoints')
        waypoints_act.setShortcut('Ctrl+W')
        waypoints_act.setStatusTip('Switch to Waypoints Table')
        view_menu.addAction(waypoints_act)
        waypoints_act.triggered.connect(lambda: self.change_model('waypoints'))

        stations_act = view_menu.addAction(station_icon, '&Stations')
        stations_act.setShortcut('Ctrl+S')
        stations_act.setStatusTip('Switch to Stations Table')
        view_menu.addAction(stations_act)
        stations_act.triggered.connect(lambda: self.change_model('stations'))

        courses_act = view_menu.addAction('&Courses')
        courses_act.setShortcut('Ctrl+C')
        courses_act.setStatusTip('Switch to Courses Table')
        view_menu.addAction(courses_act)
        courses_act.triggered.connect(lambda: self.change_model('courses'))

        coursepoints_act = view_menu.addAction(route_icon, 'Course &Points')
        coursepoints_act.setShortcut('Ctrl+P')
        coursepoints_act.setStatusTip('Switch to Coursepoints Table')
        view_menu.addAction(coursepoints_act)
        coursepoints_act.triggered.connect(lambda: self.change_model('coursepoints'))

        units_act = view_menu.addAction('&Units')
        units_act.setShortcut('Ctrl+U')
        units_act.setStatusTip('Switch to Units Table')
        view_menu.addAction(units_act)
        units_act.triggered.connect(lambda: self.change_model('units'))

        squads_act = view_menu.addAction('S&quads')
        squads_act.setShortcut('Ctrl+Q')
        squads_act.setStatusTip('Switch to Squads Table')
        view_menu.addAction(squads_act)
        squads_act.triggered.connect(lambda: self.change_model('squads'))

        schedules_act = view_menu.addAction('Sc&hedules')
        schedules_act.setShortcut('Ctrl+H')
        schedules_act.setStatusTip('Switch to Schedules Table')
        view_menu.addAction(schedules_act)
        schedules_act.triggered.connect(lambda: self.change_model('schedules'))

        itineraries_act = view_menu.addAction('&Itineraries')
        itineraries_act.setShortcut('Ctrl+I')
        itineraries_act.setStatusTip('Switch to Itineraries Table')
        view_menu.addAction(itineraries_act)
        itineraries_act.triggered.connect(lambda: self.change_model('itineraries'))

        # MAPS MENU ############################################################
        maps_menu = self.menu_bar.addMenu('&Maps')
        import_map = maps_menu.addAction('&Import')
        import_map.setShortcut('Ctrl+I')
        import_map.setStatusTip('Find image to use for map')
        maps_menu.addAction(import_map)
        import_map.triggered.connect(self.import_map_dialog)

        settings_map = maps_menu.addAction('&Coordinates')
        settings_map.setShortcut('Ctrl+S')
        settings_map.setStatusTip('Set location coordinates of map')
        maps_menu.addAction(settings_map)
        settings_map.triggered.connect(self.map_settings)

        scores_menu = self.menu_bar.addMenu('Scoreboard')
        new_scores = scores_menu.addAction('&New')
        scores_menu.addAction(new_scores)

        help_menu = self.menu_bar.addMenu('&Help')
        about_act = help_menu.addAction(about_icon, '&About')
        about_act.setShortcut('Ctrl+A')
        about_act.setStatusTip('About Derby Runner')
        help_menu.addAction(about_act)
        #        about_act.triggered.connect(help_about)

        self.menu_bar.adjustSize()
        self.setMenuBar(self.menu_bar)
        # #UTILITIES ##########################
        # widget1 = Color('green')

        # https://www.geeksforgeeks.org/pyqt5-qcalendarwidget-getting-selected-date/?ref=lbp
        widget2 = QtWidgets.QCalendarWidget()
        widget2.setStyleSheet('font-size: 10pt; color: "green "; padding: 4px; ')
        widget2.setStyleSheet("QCalendarWidget  QAbstractItemView"
                              "{"
                              "color : black; font-size: 11pt;"
                              "}"
                              )

        self.splitter_data.setGeometry(QtCore.QRect(5, 9, 600, 600))
        self.data_tools.setGeometry(QtCore.QRect(0, 0, 800, 32))
        self.data_tools.setFixedHeight(55)
        self.data_tools.setIconSize(QSize(50, 50))

        dr = pe.MasterEditor(self.df_eveentoptions, self.df_stations, self.df_waypoints)
        self.splitter_utils.addWidget(dr)

        self.splitter_utils.addWidget(widget2)

        self.splitter_data.addWidget(self.data_tools)
        self.splitter_data.addWidget(self.table)
        widget = QWidget(flags=Qt.WindowFlags())
        widget.setLayout(self.layout_main)
        self.setCentralWidget(widget)

        atexit.register(self.goodbye)

    def my_custom_fn(self, a="HELLLO!", b=5):
        print(a, b)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    top = 750
    left = 1000
    width = 2000
    height = 1000
    window.setGeometry(QtCore.QRect(left, top, width, height))
    window.show()
    app.exec_()
