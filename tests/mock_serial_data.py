"""
Mock Serial Data Generator
For testing without Arduino
"""

import time
import random

def generate_mock_data():
    """
    Simulates data coming from the Arduino serial port.
    Format: timestamp,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,lat,lon,alt
    """
    while True:
        timestamp = time.time()
        accel = [random.uniform(-1, 1) for _ in range(3)]
        gyro = [random.uniform(-0.1, 0.1) for _ in range(3)]
        gps = [30.0, 31.0, 100.0] # Mock lat, lon, alt
        
        data = f"{timestamp},{accel[0]},{accel[1]},{accel[2]},{gyro[0]},{gyro[1]},{gyro[2]},{gps[0]},{gps[1]},{gps[2]}"
        print(data)
        time.sleep(0.1)

if __name__ == "__main__":
    generate_mock_data()
