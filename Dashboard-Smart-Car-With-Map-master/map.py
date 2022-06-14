import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from pyqtlet import L, MapWidget
from PyQt5.QtCore import *
import data
import time

class TTT(QThread):

    progress_update     = pyqtSignal(int)

    def __init__(self, ui):
        super(TTT, self).__init__()
        self.ui = ui

    def run(self):
        for coordinate in data.coordinates:
            self.ui.marker.setLatLng(coordinate)
            time.sleep(2)

class MapWindow(QWidget):
    def __init__(self):
        # Setting up the widgets and layout
        super().__init__()
        self.mapWidget = MapWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.mapWidget)
        self.setLayout(self.layout)

        # Working with the maps with pyqtlet
        self.map = L.map(self.mapWidget)
        self.map.setView([-7.299221268484248, 112.76742160320283], 10)
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(self.map)
        self.marker = L.marker(data.coordinates[0])
        self.marker.addTo(self.map)
        L.polyline(data.coordinates, {'color':'blue'}).addTo(self.map)
        self.map.clicked.connect(lambda x: print(x))
       
        self.t = TTT(self)
        self.t.start()

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())