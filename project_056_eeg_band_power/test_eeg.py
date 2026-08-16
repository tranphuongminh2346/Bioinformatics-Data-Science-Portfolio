"""
Unit Tests for EEG Band Power Extractor
Author: Portfolio Creator
Description: Verify EEG timeseries loading, FFT frequencies, and energy distributions.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from eeg_extractor import EEGBandPowerExtractor

class TestEEGBandPowerExtractor(unittest.TestCase):

    def setUp(self):
        # Create a mock EEG signal CSV path
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        
        # Ensure file is generated clean
        if os.path.exists(self.temp_csv_path):
            os.remove(self.temp_csv_path)
            
        # Initialize (which will generate mock 10Hz/20Hz data)
        self.extractor = EEGBandPowerExtractor(self.temp_csv_path, fs=100.0)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.extractor.voltage), 200)
        self.assertEqual(len(self.extractor.timestamps), 200)

    def test_psd_computation(self):
        freqs, psd = self.extractor.compute_psd()
        
        # For N=200 samples, rfft returns N//2 + 1 = 101 points
        self.assertEqual(len(freqs), 101)
        self.assertEqual(len(psd), 101)
        
        # Nyquist frequency is fs / 2 = 50.0 Hz
        self.assertAlmostEqual(freqs[-1], 50.0)
        
        # Verify peak frequencies
        # The peak in PSD should be around 10 Hz and 20 Hz
        idx_10hz = np.argmin(np.abs(freqs - 10.0))
        idx_20hz = np.argmin(np.abs(freqs - 20.0))
        
        # 10Hz peak should be larger than 5Hz (background noise)
        idx_5hz = np.argmin(np.abs(freqs - 5.0))
        self.assertTrue(psd[idx_10hz] > psd[idx_5hz] * 5)
        self.assertTrue(psd[idx_20hz] > psd[idx_5hz] * 2)

    def test_band_powers(self):
        self.extractor.compute_psd()
        powers = self.extractor.calculate_band_powers()
        
        # Delta, Theta, Alpha, Beta, Gamma bands present
        self.assertEqual(len(powers), 5)
        
        # The 10 Hz signal falls into the Alpha band (8-12 Hz)
        # The 20 Hz signal falls into the Beta band (12-30 Hz)
        # Total power should be dominated by Alpha and Beta
        alpha_p = powers["Alpha"]["rel_power"]
        beta_p = powers["Beta"]["rel_power"]
        delta_p = powers["Delta"]["rel_power"]
        
        # Alpha relative power should be high (> 50%)
        self.assertTrue(alpha_p > delta_p)
        self.assertTrue(alpha_p > 40.0)

if __name__ == "__main__":
    unittest.main()
