import sys

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

        # self.times, self.gps_vals, self.ins_vals, self.kal_vals = [], [], [], []
        
        #عشان يكون اسرع بس مش مشكله في الكود هتلاحظي هنا اني برضو خليت ال condition اللي في ال while تعليق عشان برضو مياخرش بس سرشي عنها 
        BUFFER_SIZE = 200
        self.times, self.gps_vals, self.ins_vals, self.kal_vals = deque(maxlen=BUFFER_SIZE), deque(maxlen=BUFFER_SIZE), deque(maxlen=BUFFER_SIZE), deque(maxlen=BUFFER_SIZE)

        # التايمر ( سريع وسلس)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(30)

    def update_plot(self):
        new_date = False
        # سحب البيانات من طابور مصطفى بدون تعديل في المنطق
        while not self.ui_queue.empty():
            try:
                t, gps, ins, kal = self.ui_queue.get_nowait()

                #ال print بطبيعته بطئ فممكن ياخر في معالجه الداتا 
                # print(f"Data from mostafa -> GPS : {gps} ,INS :{ins} , Kelman : {kal}")
               
                
                # إرجاع t للثواني
                self.times.append(t / 1000.0)
                self.gps_vals.append(gps)
                self.ins_vals.append(ins)
                self.kal_vals.append(kal)
    
                new_data = True
                
                # الحفاظ على آخر 200 نقطة للأداء
                # if len(self.times) > 200:
                #     self.times.pop(0)
                #     self.gps_vals.pop(0)
                #     self.ins_vals.pop(0)
                #     self.kal_vals.pop(0)
            except queue.Empty:
                break
            except Exception as e:
                print(f"Error parsing date: {e}")
                break

        # تحديث الرسم
        if new_date and len(self.item) > 0:
            self.ins_line.setData(self.times, self.ins_vals)
            self.gps_line.setData(self.times, self.gps_vals)
            self.kal_line.setData(self.times, self.kal_vals)

    def run(self):
        self.show()
        sys.exit(app.exec_())
