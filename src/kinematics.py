class Kinematics:
    def __init__(self):
        self.px = 0.0
        self.py = 0.0
        self.altitude = 0.0
        
        self.vx = 0.0
        self.vy = 0.0
        self.velocity = 0.0
        
        self.prev_ax = 0.0
        self.prev_ay = 0.0
        self.prev_az_corrected = 0.0

    def integrate(self, ax, ay, az, dt):
        az_corrected = az - 9.81

        prev_vx = self.vx
        prev_vy = self.vy
        prev_vz = self.velocity

        self.vx += ((ax + self.prev_ax) / 2.0) * dt
        self.vy += ((ay + self.prev_ay) / 2.0) * dt
        self.velocity += ((az_corrected + self.prev_az_corrected) / 2.0) * dt

        self.px += ((self.vx + prev_vx) / 2.0) * dt
        self.py += ((self.vy + prev_vy) / 2.0) * dt
        self.altitude += ((self.velocity + prev_vz) / 2.0) * dt

        self.prev_ax = ax
        self.prev_ay = ay
        self.prev_az_corrected = az_corrected

        return self.altitude, self.velocity