"""
Main Entry Point and Systems Integration Pipeline
Role: Systems Integrator (Mostafa)
Description: Implements a high-performance, thread-safe Producer-Consumer architecture 
for real-time hardware data acquisition, kinematic integration, and Kalman filtering.
"""

import threading
import time
import queue
import serial
import struct
import sys
import numpy as np
from data_types import SensorData
from kinematics import Kinematics
from kalman_filter import KalmanFilter
from visualizer import Visualizer

class SerialManager:
    def __init__(self, port='/dev/ttyACM0', baudrate=500000, mock=False):
        self.port = port
        self.baudrate = baudrate
        self.mock = mock
        self.running = False
        self.data_queue = queue.Queue(maxsize=1000)
        self.ser = None
        
        # Struct format matching C++ (Omar): 
        # Header(uint16), Timestamp(uint32), Accel_X/Y/Z(float), GPS_Alt/Vel(float), GPS_Flag(uint8)
        self.struct_format = '<HIfffffB'
        self.packet_size = struct.calcsize(self.struct_format)
        self.sync_word = 0xBBAA

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()

    def _run(self):
        if self.mock:
            self._run_mock()
            return

        while self.running:
            try:
                if not self.ser or not self.ser.is_open:
                    print(f"Connecting to {self.port} at {self.baudrate} baud...")
                    self.ser = serial.Serial(self.port, self.baudrate, timeout=None)
                    self.ser.reset_input_buffer()

                raw_bytes = self.ser.read(self.packet_size)
                
                if len(raw_bytes) == self.packet_size:
                    data_tuple = struct.unpack(self.struct_format, raw_bytes)
                    
                    if data_tuple[0] == self.sync_word:
                        data = SensorData(
                            timestamp=data_tuple[1],
                            accel_x=data_tuple[2],
                            accel_y=data_tuple[3],
                            accel_z=data_tuple[4],
                            gps_alt=data_tuple[5],
                            gps_vel=data_tuple[6],
                            gps_updated=bool(data_tuple[7])
                        )
                        
                        if not self.data_queue.full():
                            self.data_queue.put(data)
                        else:
                            try:
                                self.data_queue.get_nowait()
                                self.data_queue.put(data)
                            except queue.Empty:
                                pass
                    else:
                        print("Sync lost! Re-aligning...")
                        self.ser.read(1) 

            except serial.SerialException as e:
                print(f"Serial error: {e}. Retrying...")
                if self.ser:
                    self.ser.close()
                time.sleep(2)
            except Exception as e:
                print(f"Unexpected error in Serial thread: {e}")
                time.sleep(1)

    def _run_mock(self):
        print("Starting in MOCK mode (100Hz)...")
        import random
        start_time = int(time.time() * 1000)
        while self.running:
            current_time = int(time.time() * 1000) - start_time
            data = SensorData(
                timestamp=current_time,
                accel_x=0.0,
                accel_y=0.0,
                accel_z=random.uniform(9.0, 10.5),
                gps_alt=random.uniform(95.0, 105.0),
                gps_vel=random.uniform(-1.0, 1.0),
                gps_updated=(current_time % 1000 < 10)
            )
            
            if not self.data_queue.full():
                self.data_queue.put(data)
            time.sleep(0.01)

import csv
from datetime import datetime

class DataProcessor:
    def __init__(self, data_queue, ui_queue):
        self.data_queue = data_queue
        self.ui_queue = ui_queue
        self.kinematics = Kinematics()
        self.kf = KalmanFilter(state_dim=3, obs_dim=2)
        self.running = False
        self.last_timestamp = None
        
        # Data Logging Setup
        filename = f"flight_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.csv_file = open(filename, mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp_ms', 'Accel_Z', 'GPS_Alt_Raw', 'INS_Alt_Est', 'Kalman_Alt_Est'])

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'csv_file') and not self.csv_file.closed:
            self.csv_file.close()

    def _run(self):
        print("Data Processor started.")
        while self.running:
            try:
                data: SensorData = self.data_queue.get(timeout=0.5)
                
                if self.last_timestamp is None:
                    self.last_timestamp = data.timestamp
                    continue
                
                dt = (data.timestamp - self.last_timestamp) / 1000.0
                self.last_timestamp = data.timestamp
                
                if dt <= 0 or dt > 0.5:
                    dt = 0.01 
                
                # 1. Kinematics (Mariam)
                ins_alt, ins_vel = self.kinematics.integrate(data.accel_z, dt)
                
                # 2. Kalman Filter (Tasneem)
                self.kf.update_dt(dt)
                self.kf.predict(u=data.accel_z)
                
                if data.gps_updated:
                    self.kf.update(np.array([data.gps_alt, data.gps_vel]))
                
                state = self.kf.get_state()
                kalman_alt = state[0]
                
                # 3. Push to UI Queue (Alaa)
                if not self.ui_queue.full():
                    self.ui_queue.put((data.timestamp, data.gps_alt, ins_alt, kalman_alt))
                
                # 4. Data Logging
                self.csv_writer.writerow([data.timestamp, data.accel_z, data.gps_alt, ins_alt, kalman_alt])
                
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Error in Data Processor: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Rocket GPS-INS Fusion System")
    parser.add_argument("--port", default="COM3", help="Serial port")
    parser.add_argument("--mock", action="store_true", help="Run with mock data")
    args = parser.parse_args()

    print("--- Rocket GPS-INS Fusion ---")
    
    ui_queue = queue.Queue(maxsize=1000)
    serial_mgr = SerialManager(port=args.port, mock=args.mock)
    processor = DataProcessor(serial_mgr.data_queue, ui_queue)

    serial_mgr.start()
    processor.start()

    # Visualizer must run on the main thread
    print("Starting Visualizer...")
    vis = Visualizer(ui_queue)
    vis.run()

    # Cleanup after GUI closes
    print("Stopping system components...")
    serial_mgr.stop()
    processor.stop()

if __name__ == "__main__":
    main()
