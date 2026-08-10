"""
Unit Tests for Patient Admission Forecaster
Author: Portfolio Creator
Description: Verify date indexing, backtest metrics calculations, and future forecast arrays.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forecaster import PatientAdmissionForecaster

class TestPatientAdmissionForecaster(unittest.TestCase):

    def setUp(self):
        # Create a mock dataset of 20 daily admissions
        # Using a simple repeating trend + seasonality
        dates = pd.date_range(start="2026-01-01", periods=20, freq='D')
        admissions = [40, 42, 45, 43, 50, 58, 60, 41, 43, 46, 44, 51, 59, 61, 42, 44, 47, 45, 52, 60]
        
        self.mock_data = pd.DataFrame({
            "date": dates,
            "admissions": admissions
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.forecaster = PatientAdmissionForecaster(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.forecaster.df), 20)
        self.assertTrue(isinstance(self.forecaster.df.index, pd.DatetimeIndex))
        self.assertEqual(self.forecaster.df.index.freqstr, 'D')

    def test_validation_evaluation(self):
        # Validate on 5 days (train size = 15, validation size = 5)
        metrics = self.forecaster.evaluate_validation(order=(1, 1, 0), val_days=5)
        
        self.assertIn("mae", metrics)
        self.assertIn("rmse", metrics)
        self.assertTrue(metrics["mae"] >= 0.0)
        self.assertEqual(len(metrics["predictions"]), 5)
        self.assertEqual(len(metrics["actuals"]), 5)

    def test_forecast_future(self):
        # Forecast 7 days out-of-sample
        forecast = self.forecaster.forecast_future(order=(1, 1, 0), steps=7)
        
        self.assertEqual(len(forecast), 7)
        # Check index values are dates starting from 2026-01-21
        self.assertEqual(forecast.index[0], pd.Timestamp("2026-01-21"))

if __name__ == "__main__":
    unittest.main()
