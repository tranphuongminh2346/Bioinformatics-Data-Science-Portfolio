"""
Unit Tests for Cell Migration Tracker
Author: Portfolio Creator
Description: Verify velocity, path lengths, directionality ratios, and MSD lag calculations.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from particle_tracker import CellMigrationTracker

class TestCellMigrationTracker(unittest.TestCase):

    def setUp(self):
        # Create a mock cell track (1 cell, 4 frames)
        # Linear movement: (0,0) -> (3,4) -> (6,8) -> (9,12)
        # Step size = sqrt(3^2 + 4^2) = 5.0 units.
        # Total path = 15.0 units.
        # Net displacement = sqrt(9^2 + 12^2) = 15.0 units.
        # Directionality = 15.0 / 15.0 = 1.0 (perfectly linear)
        self.mock_data = pd.DataFrame({
            "cell_id": [1, 1, 1, 1],
            "frame": [0, 1, 2, 3],
            "x": [0.0, 3.0, 6.0, 9.0],
            "y": [0.0, 4.0, 8.0, 12.0]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.tracker = CellMigrationTracker(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.tracker.cells), 1)
        self.assertIn(1, self.tracker.cells)

    def test_metrics(self):
        metrics = self.tracker.calculate_metrics(1)
        
        self.assertAlmostEqual(metrics["avg_velocity"], 5.0)
        self.assertAlmostEqual(metrics["total_path"], 15.0)
        self.assertAlmostEqual(metrics["net_displacement"], 15.0)
        self.assertAlmostEqual(metrics["directionality"], 1.0)
        
        # Directionality must be <= 1.0 always
        self.assertTrue(0.0 <= metrics["directionality"] <= 1.0)

    def test_msd(self):
        # Calculate MSD up to lag 2
        # Lag 1: differences: (3,4), (3,4), (3,4) -> all squared displacements = 25.0 -> MSD(1) = 25.0
        # Lag 2: differences: (6,8), (6,8) -> all squared displacements = 100.0 -> MSD(2) = 100.0
        msd = self.tracker.calculate_msd(1, max_lag=2)
        
        self.assertEqual(len(msd), 3)
        self.assertEqual(msd[0], 0.0)
        self.assertAlmostEqual(msd[1], 25.0)
        self.assertAlmostEqual(msd[2], 100.0)

if __name__ == "__main__":
    unittest.main()
