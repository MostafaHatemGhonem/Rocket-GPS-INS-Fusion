import sys
import threading
import queue
from collections import deque
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg

app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class Visualizer(QMainWindow):
    def __init__(self, ui_queue):
        super().__init__()
        self.ui_queue = ui_queue
        
        self.setWindowTitle("نظام تتبع مسار الصاروخ - تيم المصاعيق")
        self.resize(1200, 800) # Made the window slightly larger to fit 4 plots
        self.setStyleSheet("background-color: #121212;") 
        
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.title_label = QLabel("ROCKET TELEMETRY REAL-TIME DATA")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #00D4FF; font-weight: bold; font-size: 18px; letter-spacing: 2px;")
        self.layout.addWidget(self.title_label)
        
        # --- NEW: Graphics Layout for Multiple Plots ---
        self.win = pg.GraphicsLayoutWidget()
        self.win.setBackground('#121212')
        self.layout.addWidget(self.win)
        
        styles = {"color": "#A0A0A0", "font-size": "12px"}

        # 1. Top Left: GPS Only
        self.plot_gps = self.win.addPlot(title="1. Raw GPS Altitude")
        self.plot_gps.showGrid(x=True, y=True, alpha=0.2)
        self.plot_gps.setLabel("left", "Altitude (m)", **styles)
        self.gps_line_single = self.plot_gps.plot(pen=pg.mkPen(color='#00D4FF', width=2))

        # 2. Top Right: INS Only
        self.plot_ins = self.win.addPlot(title="2. Raw INS Kinematics")
        self.plot_ins.showGrid(x=True, y=True, alpha=0.2)
        self.plot_ins.setLabel("left", "Altitude (m)", **styles)
        self.ins_line_single = self.plot_ins.plot(pen=pg.mkPen(color='#FF00FF', width=2))

        self.win.nextRow() # Move to the bottom row

        # 3. Bottom Left: Kalman Only
        self.plot_kal = self.win.addPlot(title="3. Kalman Filter (Smoothed)")
        self.plot_kal.showGrid(x=True, y=True, alpha=0.2)
        self.plot_kal.setLabel("left", "Altitude (m)", **styles)
        self.plot_kal.setLabel("bottom", "Time (s)", **styles)
        self.kal_line_single = self.plot_kal.plot(pen=pg.mkPen(color='#39FF14', width=2))

        # 4. Bottom Right: Combined Fusion
        self.plot_comb = self.win.addPlot(title="4. Sensor Fusion Overview")
        self.plot_comb.showGrid(x=True, y=True, alpha=0.2)
        self.plot_comb.addLegend(offset=(10, 10))
        self.plot_comb.setLabel("left", "Altitude (m)", **styles)
        self.plot_comb.setLabel("bottom", "Time (s)", **styles)
        
        self.ins_line_comb = self.plot_comb.plot(pen=pg.mkPen(color='#FF00FF', width=2), name="INS")
        self.gps_line_comb = self.plot_comb.plot(pen=pg.mkPen(color='#00D4FF', width=1, style=Qt.DotLine), name="GPS")
        self.kal_line_comb = self.plot_comb.plot(pen=pg.mkPen(color='#39FF14', width=3), name="Kalman")

        # Buffers
        self.times = deque()
        self.gps_vals = deque()
        self.ins_vals = deque()
        self.kal_vals = deque()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(30)

    def update_plot(self):
        new_data = False
        while not self.ui_queue.empty():
            try:
                t, gps, ins, kal = self.ui_queue.get_nowait()

                self.times.append(t / 1000.0)
                self.gps_vals.append(gps)
                self.ins_vals.append(ins)
                self.kal_vals.append(kal)
    
                new_data = True
            except queue.Empty:
                break
            except Exception as e:
                print(f"Error parsing data: {e}")
                break

        if new_data and len(self.times) > 0:
            t_list = list(self.times)
            
            # Update Individual Plots
            self.gps_line_single.setData(t_list, list(self.gps_vals))
            self.ins_line_single.setData(t_list, list(self.ins_vals))
            self.kal_line_single.setData(t_list, list(self.kal_vals))
            
            # Update Combined Plot
            self.ins_line_comb.setData(t_list, list(self.ins_vals))
            self.gps_line_comb.setData(t_list, list(self.gps_vals))
            self.kal_line_comb.setData(t_list, list(self.kal_vals))

    def run(self):
        self.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    import random
    import time
    
    q = queue.Queue()
    
    def produce_mock_data():
        start_time = time.time() * 1000
        while True:
            t = time.time() * 1000 - start_time
            gps = 100 + random.uniform(-1, 1)
            ins = 100 + random.uniform(-2, 2)
            kal = 100 + random.uniform(-0.5, 0.5)
            q.put((t, gps, ins, kal))
            time.sleep(0.01)

    threading.Thread(target=produce_mock_data, daemon=True).start()
    
    vis = Visualizer(q)
    vis.run()