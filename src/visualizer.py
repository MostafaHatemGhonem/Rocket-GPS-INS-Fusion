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
        
        self.setWindowTitle("نظام تتبع مسار الصاروخ -  تيم المصاعيق ")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #121212;") 
         
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.title_label = QLabel("ROCKET TELEMETRY REAL-TIME DATA")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #00D4FF; font-weight: bold; font-size: 18px; letter-spacing: 2px;")
        self.layout.addWidget(self.title_label)
        
        self.graph = pg.PlotWidget()
        self.layout.addWidget(self.graph)
        
        self.graph.setBackground('#121212') 
        self.graph.showGrid(x=True, y=True, alpha=0.2) 
        self.graph.addLegend(offset=(30, 30))
        
        styles = {"color": "#A0A0A0", "font-size": "12px"}
        self.graph.setLabel("left", "Altitude (m)", **styles)
        self.graph.setLabel("bottom", "Time (s)", **styles)

        self.ins_line = self.graph.plot(pen=pg.mkPen(color='#FF00FF', width=2), name="INS ")
        self.gps_line = self.graph.plot(pen=pg.mkPen(color='#00D4FF', width=1, style=Qt.DotLine), name="GPS ")
        self.kal_line = self.graph.plot(pen=pg.mkPen(color='#39FF14', width=3), name="Kalman Filter ")

        # *** FIX: Increased buffer to 2000 to show 20 seconds of flight history at 100Hz ***
        BUFFER_SIZE = 2000
        self.times = deque(maxlen=BUFFER_SIZE)
        self.gps_vals = deque(maxlen=BUFFER_SIZE)
        self.ins_vals = deque(maxlen=BUFFER_SIZE)
        self.kal_vals = deque(maxlen=BUFFER_SIZE)

        # Timer (Fast and smooth at 30ms / ~33 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(30)

    def update_plot(self):
        new_data = False
        # سحب البيانات من طابور مصطفى بدون تعديل في المنطق
        # This logic is actually perfect! It prevents the UI from lagging behind the data.
        while not self.ui_queue.empty():
            try:
                t, gps, ins, kal = self.ui_queue.get_nowait()

                # إرجاع t للثواني
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

        # تحديث الرسم
        if new_data and len(self.times) > 0:
            self.ins_line.setData(list(self.times), list(self.ins_vals))
            self.gps_line.setData(list(self.times), list(self.gps_vals))
            self.kal_line.setData(list(self.times), list(self.kal_vals))

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
            time.sleep(0.01) # Matched mock to 100Hz

    threading.Thread(target=produce_mock_data, daemon=True).start()
    
    vis = Visualizer(q)
    vis.run()