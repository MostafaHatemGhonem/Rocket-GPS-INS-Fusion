"""
Real-time Visualization with PyQtGraph
Assigned to: Alaa
"""

import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
import sys

class Visualizer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rocket GPS-INS Fusion Visualizer")
        
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        self.x = list(range(100))
        self.y = [0] * 100
        self.data_line = self.graphWidget.plot(self.x, self.y)
        
    def update_plot(self, new_data):
        self.y = self.y[1:]
        self.y.append(new_data)
        self.data_line.setData(self.x, self.y)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    v = Visualizer()
    v.show()
    sys.exit(app.exec_())
