"""
Unit Tests for Log Autoencoder
Author: Portfolio Creator
Description: Verify StandardScalers, MLPRegressor auto-associative fits, and anomaly classifications.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from autoencoder import LogAutoencoder

class TestLogAutoencoder(unittest.TestCase):

    def setUp(self):
        # Create a mock server logs dataset of 15 records
        # 14 normal entries
        # 1 huge anomaly at index 7 (representing cpu=99%, memory=99%, io=500, net=2000)
        cpu = [15.0, 18.0, 12.0, 20.0, 25.0, 14.0, 17.0, 99.0, 11.0, 20.0, 23.0, 16.0, 19.0, 13.0, 21.0]
        memory = [42.0, 45.0, 40.0, 48.0, 50.0, 43.0, 44.0, 99.0, 39.0, 47.0, 49.0, 43.0, 45.0, 41.0, 47.0]
        disk_io = [12.0, 15.0, 10.0, 18.0, 20.0, 11.0, 13.0, 500.0, 9.0, 17.0, 19.0, 12.0, 16.0, 10.0, 18.0]
        network = [150.0, 165.0, 130.0, 180.0, 210.0, 142.0, 158.0, 2000.0, 125.0, 175.0, 202.0, 152.0, 168.0, 135.0, 179.0]
        
        self.mock_data = pd.DataFrame({
            "cpu_pct": cpu,
            "memory_pct": memory,
            "disk_io": disk_io,
            "network_traffic": network
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.detector = LogAutoencoder(self.temp_csv_path, hidden_layers=(4, 2, 4))

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.detector.df), 15)

    def test_autoencoder_fit(self):
        # Fit network
        reconstructed = self.detector.train_autoencoder()
        self.assertTrue(self.detector.is_trained)
        self.assertEqual(reconstructed.shape, (15, 4))

    def test_anomaly_classification(self):
        self.detector.train_autoencoder()
        losses = self.detector.calculate_reconstruction_errors()
        
        # Verify 15 losses
        self.assertEqual(len(losses), 15)
        
        # Anomaly at index 7 should have a much larger loss than normal logs
        self.assertTrue(losses[7] > np.mean(losses) * 2)
        
        # Flag anomalies above 90th percentile
        anom = self.detector.flag_anomalies(threshold_percentile=90.0)
        # Should flag the single anomaly
        self.assertIn(7, anom.index)
        
        # Single vector predict check
        normal_vec = [15.0, 42.0, 12.0, 150.0]
        anom_vec = [99.0, 99.0, 500.0, 2000.0]
        
        loss_normal = self.detector.predict_single_log(normal_vec)
        loss_anom = self.detector.predict_single_log(anom_vec)
        self.assertTrue(loss_anom > loss_normal * 10)

if __name__ == "__main__":
    unittest.main()
