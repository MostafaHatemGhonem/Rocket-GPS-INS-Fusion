"""
Main Entry Point and Threads
Assigned to: Mostafa
"""

import threading
import time
from kinematics import Kinematics
from kalman_filter import KalmanFilter
# from visualizer import Visualizer

def data_processing_thread():
    kin = Kinematics()
    kf = KalmanFilter(state_dim=6, obs_dim=3)
    
    while True:
        # 1. Read Serial Data (from Arduino or Mock)
        # 2. Update Kinematics
        # 3. Apply Kalman Filter
        # 4. Send to Visualizer
        print("Processing data...")
        time.sleep(1)

def main():
    print("Starting Rocket-GPS-INS-Fusion...")
    
    # Start background processing thread
    t = threading.Thread(target=data_processing_thread, daemon=True)
    t.start()
    
    # In a real scenario, the GUI (Visualizer) would run here on the main thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()
