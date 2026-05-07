"""
Kinematics and INS Integration
Assigned to: Mariam
"""
import numpy as np

class Kinematics:
    def __init__(self):
        """
        Initialize the state variables for the CubeSat/Rocket.
        """
        # Position variables
        self.px = 0.0
        self.py = 0.0
        self.altitude = 0.0  # pz
        
        # Velocity variables
        self.vx = 0.0
        self.vy = 0.0
        self.velocity = 0.0  # vz

    def integrate(self, ax, ay, az, dt):
        """
        Numerical integration using Euler method to update 
        velocity and position based on acceleration data.
        """
        
        # 1. Gravity Compensation
        # Adjust vertical acceleration to remove the effect of Earth's gravity
        az_corrected = az - 9.81

        # 2. Update Velocities (v = v0 + a * dt)
        self.vx += ax * dt
        self.vy += ay * dt
        self.velocity += az_corrected * dt

        # 3. Update Positions (p = p0 + v * dt)
        self.px += self.vx * dt
        self.py += self.vy * dt
        self.altitude += self.velocity * dt

        # Return the vertical state as per the original template requirements
        return self.altitude, self.velocity
