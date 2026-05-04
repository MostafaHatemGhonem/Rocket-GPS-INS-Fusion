import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import collections
import queue
import sys

class Visualizer:
    def __init__(self, ui_queue: queue.Queue):
        # TODO: Alaa - This is your playground!
        # Your objective:
        # 1. Setup a PyQtGraph window and plot.
        # 2. Use a QTimer to periodically pull data from 'self.ui_queue'.
        # 3. Update the plot curves with the incoming data.
        # Data format in the queue: (timestamp_ms, gps_alt, ins_alt, kalman_alt)
        
        self.ui_queue = ui_queue
        print("Visualizer Initialized. Alaa, it's your turn to build the GUI!")

    def run(self):
        """
        This method is called from main.py to start the GUI event loop.
        """
        # TODO: Alaa - Initialize your QApplication and start the event loop here.
        # Example: 
        # self.app = QtWidgets.QApplication(sys.argv)
        # ... your code ...
        # sys.exit(self.app.exec_())
        pass

if __name__ == "__main__":
    # You can test your visualizer independently here
    q = queue.Queue()
    v = Visualizer(q)
    v.run()
