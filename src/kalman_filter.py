"""
Kalman Filter Matrices and Logic
Assigned to: Tasneem
"""

import numpy as np

class KalmanFilter:
    def __init__(self, state_dim=3, obs_dim=2):
        # TODO: Tasneem - Define your state vector dimensions and matrices
        # State typically: [Altitude, Velocity, AccelBias]
        self.x = np.zeros(state_dim)  # State estimate
        self.P = np.eye(state_dim)    # State covariance
        self.F = np.eye(state_dim)    # State transition matrix
        self.H = np.zeros((obs_dim, state_dim)) # Observation matrix
        self.R = np.eye(obs_dim)      # Measurement noise
        self.Q = np.eye(state_dim)    # Process noise
        self.dt = 0.01

    def update_dt(self, dt):
        """
        Update the state transition matrix F and process noise Q based on dynamic dt.
        """
        self.dt = dt
        # TODO: Tasneem - Update F and Q matrices based on the new dt
        pass

    def predict(self, u=0.0):
        """
        Predict the next state using control input u (acceleration).
        """
        # TODO: Tasneem - Implement the Prediction step: x = Fx + Bu, P = FPF' + Q
        pass

    def update(self, z):
        """
        Update the state with a new measurement vector z (e.g., [gps_alt, gps_vel]).
        """
        # TODO: Tasneem - Implement the Update step: K = PH'(HPH' + R)^-1, x = x + K(z - Hx), P = (I - KH)P
        pass
    
    def get_state(self):
        # Returns the current state estimate
        return self.x
