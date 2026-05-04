"""
Kinematics and INS Integration
Assigned to: Mariam
"""

import numpy as np

class Kinematics:
    def __init__(self):
        # TODO: Mariam - Initialize your state variables here
        self.altitude = 0.0
        self.velocity = 0.0

    def integrate(self, accel_z, dt):
        """
        Integrate vertical acceleration to update altitude and velocity.
        """
        # TODO: Mariam - Implement your integration logic here (e.g., Euler or RK4)
        # Remember to handle gravity compensation!
        
        return self.altitude, self.velocity
