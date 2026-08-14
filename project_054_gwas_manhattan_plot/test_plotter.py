"""
Unit Tests for GWAS Plotter
Author: Portfolio Creator
Description: Verify p-value log-transforms, Bonferroni significance corrections, and filters.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gwas_plotter import GWASPlotter

class TestGWASPlotter(unittest.TestCase):

    def setUp(self):
        # Create a mock GWAS dataset (10 records)
        # N = 10 -> Bonferroni threshold = 0.05 / 10 = 0.005
        # 1 variant (rs10) has p_value = 0.001 (significant)
        chrom = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
        pos = [100, 200, 300, 100, 200, 100, 200, 100, 200, 100]
        rsid = [f"rs{i}" for i in range(1, 11)]
        p_value = [0.5, 0.2, 0.01, 0.8, 0.4, 0.001, 0.3, 0.9, 0.1, 0.05]
        
        self.mock_data = pd.DataFrame({
            "chrom": chrom,
            "pos": pos,
            "rsid": rsid,
            "p_value": p_value
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.plotter = GWASPlotter(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.plotter.df), 10)
        # Check negative log conversion: p_val = 0.01 -> -log10(0.01) = 2.0
        self.assertAlmostEqual(self.plotter.df.loc[2, 'neg_log_p'], 2.0)

    def test_bonferroni_threshold(self):
        # N = 10 -> thresh = 0.005
        thresh = self.plotter.get_bonferroni_threshold(0.05)
        self.assertEqual(thresh, 0.005)

    def test_filter_significance(self):
        sig = self.plotter.get_significant_variants(0.05)
        
        # Only rs6 has P = 0.001 <= 0.005
        self.assertEqual(len(sig), 1)
        self.assertEqual(sig.iloc[0]['rsid'], "rs6")

if __name__ == "__main__":
    unittest.main()
