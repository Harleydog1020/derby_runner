# from https://stackoverflow.com/questions/33569626/matplotlib-responding-to-click-events
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PIL import Image

class Communicator(QWidget):
    # https://realpython.com/python-pyqt-layout/#nesting-layouts-to-build-complex-guis
    def __init__(self):
        super(Communicator, self).__init__()
        self.v_box = QVBoxLayout()

        self.page_combo = QComboBox()
        self.page_combo.addItems(['Station', 'Waypoint'])
        self.page_combo.activated.connect(self.switch_page)
        self.stacked_layout = QStackedLayout()
        self.station_page = QWidget()
        self.station_layout = QFormLayout()
        self.station_layout.addRow('Description: ', QLineEdit())
        self.station_page.setLayout(self.station_layout)
        self.stacked_layout.addWidget(self.station_page)

        self.waypoint_page = QWidget()
        self.waypoint_layout = QFormLayout()
        self.waypoint_layout.addRow('Marker: ', QLineEdit())
        self.waypoint_page.setLayout(self.waypoint_layout)
        self.stacked_layout.addWidget(self.waypoint_page)

        self.comm_layout = QFormLayout()
        self.Name = QLineEdit()
        self.comm_layout.addRow(QLabel("Name: "), self.Name)
        self.Longitude = QLineEdit()
        self.Latitude = QLineEdit()
        self.comm_layout.addRow(QLabel("Longitude: "), self.Longitude)
        self.comm_layout.addRow(QLabel("Latitude: "), self.Latitude)
        self.v_box.addLayout(self.comm_layout)
        self.v_box.addWidget(self.page_combo)
        self.v_box.addLayout(self.stacked_layout)
        self.setLayout(self.v_box)

    def change_widget(self, x, y):
        self.Longitude.setText(str(x))
        self.Latitude.setText(str(y))

    def switch_page(self):
        self.stacked_layout.setCurrentIndex(self.page_combo.currentIndex())


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

        self.image = Image.open("/home/brickyard314/DerbyRunner/CampHart.png", 'r')
        self.ax.imshow(self.image, extent=[-75.428953, -75.422756, 40.362168, 40.36787])
        self.ax.set_title('Derby Runner Map')
        self.x_points = x_points
        self.y_points = y_points
        self.pointset, = self.ax.plot(self.x_points, self.y_points, 'o',
                                      picker=True, pickradius=5)

class MasterEditor(QWidget):
    def __init__(self, df_eveentoptions, df_stations, df_waypoints):
        super().__init__()

        self.cidkey = None
        self.cidrelease = None
        self.cidpress = None
        self.pe_box = QHBoxLayout()
        # https://datatofish.com/convert-string-to-float-dataframe/
        # subset stations to Name, Longitude and Latitude
        # add a column and fill it with 'Stations'
        # subset waypoints to Name, Longitude and Latitude
        # add the same column but fill it with 'Waypoints'
        # now append the Waypoints dataframe to the Stations dataframe
        x = pd.to_numeric(df_stations['Longitude'], errors='coerce')
        x = x.dropna()
        self.x_points = x.to_numpy()
        y = pd.to_numeric(df_stations['Latitude'], errors='coerce')
        y = y.dropna()
        self.y_points = y.to_numpy()

        # self.y_points = np.array([])
        print("XPoints: ")
        print(self.x_points)
        print("YPoints: ")
        print(self.y_points)
        self.setup_map()

    def setup_map(self):
        self.pe = PointEditor(x_points=self.x_points, y_points=self.y_points)
        print("XPoints: ")
        print(self.x_points)
        print("YPoints: ")
        print(self.y_points)
        self.d_info = Communicator()
        self.d_info.setGeometry(QtCore.QRect(0, 0, 800, 800))
        self.d_info.setStyleSheet(
            'font-size: 12pt; color: "black"; padding: 4px; margin: 2px; border: 1px solid #5CACEE;'
            'selection-background-color: #1B89CA; selection-color: #F0F0F0;')
        self.pe_box.addWidget(self.pe)
        self.pe_box.addWidget(self.d_info)
        self.setLayout(self.pe_box)
        self.connect()
        return

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

    def on_key(self, event):
        """
        Function to be bound to the key press event
        If the key pressed is 'Del' and there is a picked object,
        remove that object from the canvas
        """
        if event.key == u'delete':
            # self.ax = plt.gca()
            if self.ax.picked_object:
                self.ax.picked_object.remove()
                self.ax.picked_object = None
                # self.ax.figure.canvas.draw()

    def on_motion(self, event):
        print("moving!")

    def on_release(self, event):
        """Clear button press information."""
        press = None
        # self.fig.canvas.draw()

    def plot_point(self, xpoint, ypoint):
        # self.ax = plt.gca()
        # fig, ax = plt.subplots()
        self.pe.x_points = np.append(self.pe.x_points, np.array(xpoint))
        self.pe.y_points = np.append(self.pe.y_points, np.array(ypoint))
        # 'v'  '8' '*'
        self.pe.pointset, = self.pe.ax.plot(self.pe.x_points, self.pe.y_points, 'P', color='green', markersize=8,
                                            picker=True, pickradius=5)
        self.pe.ax.figure.canvas.draw()

    def display_info(self, xpoint, ypoint):
        self.d_info.change_widget(xpoint, ypoint)

    def onclick(self, event):
        """
        These implement click functionality.
        """
        if event.dblclick:
            if event.inaxes != self.ipoint.axes:
                return
            contains, attrd = self.ipoint.contains(event)
            if not contains:
                return

        else:
            if event.button == 1:
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

                for xp, yp in zip(xpix, ypix):
                    distance = (abs(expix - xp) ** 2 + abs(eypix - yp) ** 2) ** 0.5
                    if distance < 10:
                        Found = True
                        event.xdata = xp
                        event.ydata = yp

                if Found:
                    print("Found, now open dialog prepopulated with point info")
                else:
                    print("New Point Added, now open dialog to add point info, prepopulate coordinates as read-only")
                    self.plot_point(event.xdata, event.ydata)
                    self.display_info(event.xdata, event.ydata)

            elif event.button == 3:

                self.point_dialog(event.xdata, event.ydata, False)
        return

 # ##############################################################################
# First we need to catch three types of event, clicks, "picks" (a specialised
# type of click to select an object on a matplotlib canvas) and key presses.
# The logic is - if it's a right double click, wait for the next click and draw
# a line, if it is a right double click draw a fixed radius circle.  If it's a
# pick, store a reference to the picked item until the next keypress.  If it's
# a keypress - test if it's delete and if so, remove the picked object.
# The functions (defined above) bound to the events implement this logic
# button_press = fig.canvas.mpl_connect('button_press_event', onclick)
# Connect to all the events we need
# set the size of the matplotlib figure in data units, so that it doesn't
# auto-resize (which will be the default on the first drawn item)


# ax.aspect = 1
# plt.tight_layout()
# x_points = np.array([])
# y_points = np.array([])
# dr = PointEditor(x_points, y_points)
# dr.connect()

# main_window = QMainWindow()
# main_window.layout_main = QHBoxLayout()
# splitter_main = QSplitter(Qt.Horizontal)
# main_window.layout_main.addWidget(splitter_main)
# plt.show()
