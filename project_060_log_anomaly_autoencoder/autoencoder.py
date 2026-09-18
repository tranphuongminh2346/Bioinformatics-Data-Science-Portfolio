"""
Neural Network Autoencoder Log Anomaly Detector
Author: Portfolio Creator
Description: Fits standard scalers and scikit-learn MLPRegressor autoencoders (X -> X)
             to compute reconstruction errors and flag server metrics anomalies.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

class LogAutoencoder:
    """Neural network autoencoder for unsupervised metric anomaly detection."""
    
    def __init__(self, data_path: str, hidden_layers: tuple = (4, 2, 4)):
        self.data_path = data_path
        self.hidden_layers = hidden_layers
        self.df = None
        self.features = ['cpu_pct', 'memory_pct', 'disk_io', 'network_traffic']
        
        self.scaler = StandardScaler()
        self.model = None
        self.is_trained = False
        
        self.load_data()

    def load_data(self):
        """Loads hourly server performance logs from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Server logs file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)

    def train_autoencoder(self) -> np.ndarray:
        """
        Fits StandardScaler and MLPRegressor as an auto-associative network (X -> X).
        
        Returns:
            np.ndarray: Reconstructed scaled features matrix.
        """
        X = self.df[self.features].values
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit MLPRegressor mapping X_scaled -> X_scaled
        self.model = MLPRegressor(
            hidden_layer_sizes=self.hidden_layers,
            activation='tanh',
            solver='adam',
            max_iter=400,
            random_state=42
        )
        
        self.model.fit(X_scaled, X_scaled)
        self.is_trained = True
        
        X_reconstructed = self.model.predict(X_scaled)
        return X_reconstructed

    def calculate_reconstruction_errors(self) -> np.ndarray:
        """
        Computes row-wise Mean Squared Error (MSE) reconstruction losses.
        
        Returns:
            np.ndarray: Array of reconstruction losses.
        """
        if not self.is_trained:
            self.train_autoencoder()
            
        X = self.df[self.features].values
        X_scaled = self.scaler.transform(X)
        X_reconstructed = self.model.predict(X_scaled)
        
        # Calculate mean squared difference per row
        losses = np.mean((X_scaled - X_reconstructed) ** 2, axis=1)
        self.df['reconstruction_loss'] = losses
        return losses

    def flag_anomalies(self, threshold_percentile: float = 90.0) -> pd.DataFrame:
        """
        Flags logs with reconstruction losses exceeding the target percentile threshold.
        
        Returns:
            pd.DataFrame: DataFrame containing flagged anomaly records.
        """
        if 'reconstruction_loss' not in self.df.columns:
            self.calculate_reconstruction_errors()
            
        threshold = np.percentile(self.df['reconstruction_loss'], threshold_percentile)
        self.df['is_anomaly'] = self.df['reconstruction_loss'] > threshold
        return self.df[self.df['is_anomaly']].copy()
        
    def predict_single_log(self, log_vector: list) -> float:
        """Predicts the reconstruction loss for a single log metrics vector."""
        if not self.is_trained:
            self.train_autoencoder()
            
        scaled_log = self.scaler.transform([log_vector])
        reconstructed = self.model.predict(scaled_log)
        loss = np.mean((scaled_log - reconstructed) ** 2)
        return float(loss)
