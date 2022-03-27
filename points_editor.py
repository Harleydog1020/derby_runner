# from https://stackoverflow.com/questions/33569626/matplotlib-responding-to-click-events
import matplotlib.pyplot as plt
import numpy as np
import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Communicator(QWidget):
    def __init__(self):
        super(Communicator, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('red'))
        self.setPalette(palette)
        self.v_box = QVBoxLayout()
        self.v_box.setAlignment(QtCore.Qt.AlignTop)
        self.station_box = QFormLayout()
        self.comm_layout = QFormLayout()
        self.comm_layout.setAlignment(QtCore.Qt.AlignTop)
        self.radio_box = QHBoxLayout()
        self.rbtn1 = QRadioButton('Station')
        self.rbtn2 = QRadioButton('Waypoint')
        self.rbtn1.toggled.connect(self.StationClicked)
        self.rbtn2.toggled.connect(self.WaypointClicked)
        self.radio_box.addWidget(self.rbtn1)
        self.radio_box.addWidget(self.rbtn2)
        self.comm_layout.addRow(self.radio_box)
        self.Name = QLineEdit()
        self.comm_layout.addRow(QLabel("Name: "), self.Name)
        self.Desc = QLineEdit()
        self.station_box.addRow(QLabel("Description: "), self.Desc)
        self.comm_layout.addRow(self.station_box)
        self.Longitude = QLineEdit()
        self.Latitude = QLineEdit()
        self.comm_layout.addRow(QLabel("Longitude: "), self.Longitude)
        self.comm_layout.addRow(QLabel("Latitude: "), self.Latitude)

        self.v_box.addLayout(self.comm_layout)
        self.setLayout(self.v_box)
        self.ChangeWidget(0, 0)

    def ChangeWidget(self, x, y):
        self.Longitude.setText(str(x))
        self.Latitude.setText(str(y))

    def StationClicked(self):
        self.Desc = QLineEdit()
        self.station_box.addRow(QLabel("Description: "), self.Desc)

    def WaypointClicked(self):
        self.station_box.removeRow(self.Desc)

class PointEditor(FigureCanvas):

    def __init__(self, x_points, y_points, parent=None):

        fig, ax = plt.subplots()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.fig = fig
        self.ax = ax
        self.ax.set_title('click on points')
        self.ax.set_xlim([0, 2])
        self.ax.set_ylim([0, 2])
        # self.x_points = np.array([])
        self.x_points = x_points
        # self.y_points = np.array([])
        self.y_points = y_points
        self.pointset, = self.ax.plot(self.x_points, self.y_points, 'o',
                           picker=True, pickradius=5)




class master_editor(QWidget):
    def __init__(self):
        super().__init__()

        pe_box = QHBoxLayout()
        x_points = np.array([])
        y_points = np.array([])
        self.pe = PointEditor(x_points=x_points, y_points=y_points)
        self.d_info = Communicator()
        self.d_info.setFixedHeight(200)
        pe_box.addWidget(self.pe)
        pe_box.addWidget(self.d_info)
        self.setLayout(pe_box)
        self.connect()

    def connect(self):
        """Connect to all the events we need."""
        # https://matplotlib.org/stable/users/explain/event_handling.html

        self.cidpress = self.pe.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cidrelease = self.pe.fig.canvas.mpl_connect('button_release_event', self.on_release)
        # cidmotion = fig.canvas.mpl_connect('motion_notify_event', on_motion)
        # cidpick = fig.canvas.mpl_connect('pick_event', onpick)
        self.cidkey = self.pe.fig.canvas.mpl_connect('key_press_event', self.on_key)
    def point_dialog(self, x, y, Found):
        # https://www.pythonguis.com/tutorials/pyqt-dialogs/

        dlg = QDialog()
        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        dlg.button_box = QDialogButtonBox(q_btn)
        dlg.layout = QFormLayout()
        dlg.radio_box = QHBoxLayout()
        message = QLabel("Hi there.")
        message.setAlignment(QtCore.Qt.AlignLeft)
        dlg.layout.addRow(message)

        # https://www.delftstack.com/tutorial/pyqt5/pyqt5-radiobutton/
        dlg.rbtn1 = QRadioButton('Station')
        dlg.rbtn2 = QRadioButton('Waypoint')
        dlg.radio_box.addWidget(dlg.rbtn1)
        dlg.radio_box.addWidget(dlg.rbtn2)
        dlg.layout.addRow(dlg.radio_box)

        xlabel = QLabel("Longitude: ")
        ylabel = QLabel("Latitude: ")
        dlg.longitude = QLineEdit(str(x))
        dlg.latitude = QLineEdit(str(y))
        dlg.layout.addRow(xlabel, dlg.longitude)
        dlg.layout.addRow(ylabel, dlg.latitude)

        dlg.layout.addWidget(dlg.button_box)
        dlg.setLayout(dlg.layout)
        dlg.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        dlg.setGeometry(1200, 1200, 800, 600)
        dlg.exec()



    def onpick(self, event):
        """
        Handles the pick event - if an object has been picked, store a
        reference to it.  We do this by simply adding a reference to it
        named 'stored_pick' to the axes object.  Note that in python we
        can dynamically add an attribute variable (stored_pick) to an
        existing object - even one that is produced by a library as in this
        case
        """
        # https://matplotlib.org/stable/gallery/event_handling/pick_event_demo.html
        print(event)
        this_artist = event.artist  # the picked object is available as event.artist
        print(this_artist)  # For debug just to show you which object is picked
        #plt.gca().picked_object = this_artist

    def on_key(self, event):
        """
        Function to be bound to the key press event
        If the key pressed is delete and there is a picked object,
        remove that object from the canvas
        """
        if event.key == u'delete':
            #self.ax = plt.gca()
            if self.ax.picked_object:
                self.ax.picked_object.remove()
                print(self.ax.picked_object)
                self.ax.picked_object = None
                #self.ax.figure.canvas.draw()

    def on_motion(self, event):
        print("moving!")

    def on_release(self, event):
        """Clear button press information."""
        press = None
        #self.fig.canvas.draw()

    def plot_point(self, xpoint, ypoint):
        #self.ax = plt.gca()
        #fig, ax = plt.subplots()
        self.pe.x_points = np.append(self.pe.x_points, np.array(xpoint))
        print("XP = ",str(self.pe.x_points))
        self.pe.y_points = np.append(self.pe.y_points, np.array(ypoint))
        # 'v'  '8' '*'
        self.pe.pointset, = self.pe.ax.plot(self.pe.x_points, self.pe.y_points, 'P', color='green', markersize=8, picker=True, pickradius=5)
        self.pe.ax.figure.canvas.draw()

    def display_info(self, xpoint, ypoint):
        my_str = "Xp = " + str(xpoint) + " Yp = " + str(ypoint)
        self.d_info.ChangeWidget(xpoint, ypoint)

    def onclick(self, event):
        """
        This implements click functionality.
        """
        #print(ipoint.axes)
        if event.dblclick:
            print("Double Click")
            if event.inaxes != self.ipoint.axes:
                print("Nope")
                return
            contains, attrd = self.ipoint.contains(event)
            if not contains:
                print("Double Nope")
                return
            print('event contains', self.ipoint.axes)
            #self.press = self.rect.xy, (event.xdata, event.ydata)
        else:
            print("Single Click")
            if event.button == 1:
                print("Left Click")
                Found = False
                x, y = self.pe.pointset.get_data()
                xy_pixels = self.pe.ax.transData.transform(np.vstack([x, y]).T)
                xpix, ypix = xy_pixels.T

                event_pixels = self.pe.ax.transData.transform(np.vstack([event.xdata, event.ydata]).T)
                expix, eypix = event_pixels.T

                # In matplotlib, 0,0 is the lower left corner, whereas it's usually the upper
                # left for most image software, so we'll flip the y-coords...
                width, height = self.pe.fig.canvas.get_width_height()
                ypix = height - ypix
                eypix = height - eypix
                print('Coordinates of the NEW POINT in pixel coordinates...')
                print(expix,eypix)


                for xp, yp in zip(xpix, ypix):
                    distance = (abs(expix - xp)**2 + abs(eypix - yp)**2)**0.5
                    if distance < 10:
                        Found = True
                        event.xdata = xp
                        event.ydata = yp

                if Found:
                    print("Found, now open dialog prepopulated with point info")
                else:
                    print("New Point Added, now open dialog to add point info, prepopulate coordinates as read-only")
                    self.plot_point(event.xdata, event.ydata)
                    print("Is it here?")
                    self.display_info(event.xdata, event.ydata)

            elif event.button == 3:
                print("Right Click?")
                self.point_dialog(event.xdata, event.ydata, False)
        return

# ##############################################################################
# First we need to catch three types of event, clicks, "picks" (a specialised
# type of click to select an object on a matplotlib canvas) and key presses.
# The logic is - if it's a right double click, wait for the next click and draw
# a line, if its a right double click draw a fixed radius circle.  If it's a
# pick, store a reference to the picked item until the next keypress.  If it's
# a keypress - test if it's delete and if so, remove the picked object.
# The functions (defined above) bound to the events implement this logic
# button_press = fig.canvas.mpl_connect('button_press_event', onclick)
# Connect to all the events we need
# set the size of the matplotlib figure in data units, so that it doesn't
# auto-resize (which it will be default on the first drawn item)


#ax.aspect = 1
#plt.tight_layout()
# x_points = np.array([])
# y_points = np.array([])
# dr = PointEditor(x_points, y_points)
# dr.connect()

# main_window = QMainWindow()
# main_window.layout_main = QHBoxLayout()
# splitter_main = QSplitter(Qt.Horizontal)
# main_window.layout_main.addWidget(splitter_main)
# plt.show()
