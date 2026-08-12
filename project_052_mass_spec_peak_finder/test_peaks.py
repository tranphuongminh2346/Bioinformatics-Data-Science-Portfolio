"""
Unit Tests for Mass Spectrometry Peak Finder
Author: Portfolio Creator
Description: Verify rolling baseline, noise standard deviations, and peaks identification.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from peak_finder import MassSpecPeakFinder

class TestMassSpecPeakFinder(unittest.TestCase):

    def setUp(self):
        # Create a mock spectrum of 40 points
        # Background = 50 + small noise
        # 1 single sharp peak at index 20 (mz=120) with intensity 500
        mz = np.linspace(100, 140, 40)
        intensity = np.ones(40) * 50.0
        # Add random noise
        np.random.seed(42)
        intensity += np.random.normal(0, 1, 40)
        
        # Add single peak
        intensity[20] = 500.0
        
        self.mock_data = pd.DataFrame({
            "mz": mz,
            "intensity": intensity
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.finder = MassSpecPeakFinder(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.finder.mz), 40)
        self.assertEqual(len(self.finder.intensity), 40)

    def test_baseline_correction(self):
        corrected = self.finder.remove_baseline(window_size=5)
        
        # Length must match
        self.assertEqual(len(corrected), 40)
        # Baseline should be near 50, so corrected background should be near 0
        self.assertTrue(corrected[0] < 5.0)
        # Peak at index 20 should remain high
        self.assertTrue(corrected[20] > 400.0)

    def test_noise_estimation(self):
        self.finder.remove_baseline()
        noise = self.finder.estimate_noise_std()
        
        self.assertTrue(noise > 0.0)
        # Noise should be small (close to the standard deviation of simulated normal noise, which is ~1.0)
        self.assertTrue(noise < 2.0)

    def test_peak_detection(self):
        self.finder.remove_baseline()
        self.finder.estimate_noise_std()
        
        peaks = self.finder.detect_peaks(snr_threshold=3.0, min_height=100.0)
        
        # Verify 1 peak detected
        self.assertEqual(len(peaks), 1)
        self.assertEqual(peaks[0]["index"], 20)
        self.assertAlmostEqual(peaks[0]["mz"], 120.51, places=1)
        self.assertTrue(peaks[0]["snr"] > 100.0)  # Very high SNR

if __name__ == "__main__":
    unittest.main()
