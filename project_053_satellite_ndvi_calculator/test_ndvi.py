"""
Unit Tests for Satellite NDVI Calculator
Author: Portfolio Creator
Description: Verify band dimensions, NDVI divisions, zero-handling, and cover counts.
Language: English (100%)
"""

import unittest
import os
import sys
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ndvi_calculator import NDVICalculator

class TestNDVICalculator(unittest.TestCase):

    def setUp(self):
        # Create a mock Red band matrix (3x3)
        self.mock_red = np.array([
            [0.1, 0.4, 0.0],
            [0.1, 0.4, 0.1],
            [0.1, 0.4, 0.1]
        ])
        
        # Create a mock NIR band matrix (3x3)
        self.mock_nir = np.array([
            [0.6, 0.1, 0.0],  # Cell [0,2] will have both Red and NIR = 0 (zero-division test)
            [0.5, 0.15, 0.3],
            [0.5, 0.2, 0.3]
        ])
        
        self.red_fd, self.temp_red_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.red_fd)
        np.savetxt(self.temp_red_path, self.mock_red, delimiter=',')
        
        self.nir_fd, self.temp_nir_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.nir_fd)
        np.savetxt(self.temp_nir_path, self.mock_nir, delimiter=',')
        
        self.calculator = NDVICalculator(self.temp_red_path, self.temp_nir_path)

    def tearDown(self):
        if os.path.exists(self.temp_red_path):
            try:
                os.remove(self.temp_red_path)
            except PermissionError:
                pass
        if os.path.exists(self.temp_nir_path):
            try:
                os.remove(self.temp_nir_path)
            except PermissionError:
                pass

    def test_dimensions(self):
        self.assertEqual(self.calculator.red_matrix.shape, (3, 3))
        self.assertEqual(self.calculator.nir_matrix.shape, (3, 3))

    def test_ndvi_math_and_zero_division(self):
        ndvi = self.calculator.calculate_ndvi()
        
        # Cell [0,0]: Red=0.1, NIR=0.6 -> NDVI = (0.6-0.1)/(0.6+0.1) = 0.5/0.7 = 0.714
        self.assertAlmostEqual(ndvi[0, 0], 0.7142857, places=5)
        
        # Cell [0,1]: Red=0.4, NIR=0.1 -> NDVI = (0.1-0.4)/(0.1+0.4) = -0.3/0.5 = -0.6
        self.assertAlmostEqual(ndvi[0, 1], -0.6, places=5)
        
        # Cell [0,2]: Red=0.0, NIR=0.0 -> Sum=0.0 -> NDVI should be 0.0 (protected from division by zero)
        self.assertEqual(ndvi[0, 2], 0.0)

    def test_land_cover_counts(self):
        self.calculator.calculate_ndvi()
        cats = self.calculator.classify_land_cover()
        
        # Total pixels = 9.
        # Check that percent sums to 100%
        total_pct = sum(d["percent"] for d in cats.values())
        self.assertAlmostEqual(total_pct, 100.0)
        
        # Cell [0,1] is -0.6 -> Water/Snow (NDVI < 0) -> count should be >= 1
        self.assertTrue(cats["Water/Snow"]["count"] >= 1)

if __name__ == "__main__":
    unittest.main()
