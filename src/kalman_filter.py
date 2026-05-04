"""
Kalman Filter Matrices and Logic
Assigned to: Tasneem
"""

import numpy as np

class KalmanFilter:
    def __init__(self, state_dim, obs_dim):
        self.x = np.zeros(state_dim)  # State estimate
        self.P = np.eye(state_dim)    # State covariance
        self.F = np.eye(state_dim)    # State transition matrix
        self.H = np.zeros((obs_dim, state_dim)) # Observation matrix
        self.R = np.eye(obs_dim)      # Measurement noise
        self.Q = np.eye(state_dim)    # Process noise

    def predict(self):
        """
        Predict the next state.
        """
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        """
        Update the state with a new measurement z.
        """
        y = z - np.dot(self.H, self.x)
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)
    
    def get_state(self):
        return self.x
