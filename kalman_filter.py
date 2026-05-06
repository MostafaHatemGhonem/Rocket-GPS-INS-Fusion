import numpy as np

class KalmanFilter:
    def __init__(self, dt=0.01):
        self.dt = dt

        # State: [altitude, velocity, accelerometer_bias]
        self.x = np.zeros((3, 1))

        # Covariance
        self.P = np.eye(3) * 10.0

        # Identity matrix
        self.I = np.eye(3)

        # Measurement matrix (GPS: altitude + velocity)
        self.H = np.array([
            [1, 0, 0],
            [0, 1, 0]
        ])

        # Measurement noise (GPS) ***
        self.R = np.array([
            [15.0, 0],
            [0, 5.0]
        ])

        # Initialize dynamic matrices
        self._update_matrices()

    def _update_matrices(self):
        dt = self.dt

        # State transition matrix
        self.F = np.array([
            [1, dt, -0.5 * dt**2],
            [0, 1, -dt],
            [0, 0, 1]
        ])

        # Control matrix (acceleration input)
        self.B = np.array([
            [0.5 * dt**2],
            [dt],
            [0.0]
        ])

        # Process noise (INS uncertainty) ***
        self.Q = np.array([
            [1e-4, 0, 0],
            [0, 1e-3, 0],
            [0, 0, 1e-6]
        ])

    def set_dt(self, dt):
        """Update timestep dynamically"""
        self.dt = dt
        self._update_matrices()

    def predict(self, acceleration):
        """Prediction step using INS acceleration"""
        self.x = self.F @ self.x + self.B * acceleration
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, measurement):
        """Update step using GPS measurement [altitude, velocity]"""
        z = np.array(measurement).reshape(-1, 1)

        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # State update
        self.x = self.x + K @ y

        # Joseph form (numerically stable)
        self.P = (self.I - K @ self.H) @ self.P @ (self.I - K @ self.H).T + K @ self.R @ K.T

    def get_state(self):
        """Return [altitude, velocity, bias]"""
        return self.x.flatten()