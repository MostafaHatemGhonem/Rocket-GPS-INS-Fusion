from dataclasses import dataclass
import numpy as np

@dataclass
class SensorData:
    timestamp: int      # ms from Arduino
    accel_x: float
    accel_y: float
    accel_z: float
    gps_alt: float
    gps_vel: float
    gps_updated: bool

    # We can keep a helper or property for array access if needed
    @property
    def accel_array(self):
        return np.array([self.accel_x, self.accel_y, self.accel_z])
