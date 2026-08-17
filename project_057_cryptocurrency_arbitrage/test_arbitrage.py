"""
Unit Tests for Arbitrage Detector
Author: Portfolio Creator
Description: Verify trading math, fee deductions, and circular yield calculations.
Language: English (100%)
"""

import unittest
import os
import sys
import json
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from arbitrage_detector import ArbitrageDetector

class TestArbitrageDetector(unittest.TestCase):

    def setUp(self):
        # Create a mock order book JSON database
        # 1. Profitable case in Path B (USDT -> ETH -> BTC -> USDT)
        # BTC/USDT Ask=60000, Bid=59900
        # ETH/BTC Ask=0.050, Bid=0.049
        # ETH/USDT Ask=2900, Bid=2950 (we set bid high to allow positive yield)
        self.mock_rates = {
            "BTC_USDT": {"ask": 60000.0, "bid": 59990.0},
            "ETH_BTC": {"ask": 0.050, "bid": 0.049},
            "ETH_USDT": {"ask": 2900.0, "bid": 2980.0}
        }
        
        self.db_fd, self.temp_json_path = tempfile.mkstemp(suffix=".json")
        os.close(self.db_fd)
        with open(self.temp_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.mock_rates, f)
            
        # Initialize with 0.1% fee
        self.detector = ArbitrageDetector(self.temp_json_path, trading_fee=0.001)

    def tearDown(self):
        if os.path.exists(self.temp_json_path):
            try:
                os.remove(self.temp_json_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(self.detector.rates["BTC_USDT"]["ask"], 60000.0)

    def test_fee_adjusted_yield(self):
        # Initial capital = 1000 USDT.
        # Run Path B: USDT -> ETH -> BTC -> USDT
        # Step 1: Buy ETH. Recv = (1000 / 2900) * 0.999 = 0.34448 ETH
        # Step 2: Sell ETH for BTC. Recv = (0.34448 * 0.049) * 0.999 = 0.01686 BTC
        # Step 3: Sell BTC for USDT. Recv = (0.01686 * 59990) * 0.999 = 1010.51 USDT
        # Yield should be positive (~1.05%)
        res = self.detector.check_path_b(1000.0)
        
        self.assertTrue(res["is_profitable"])
        self.assertTrue(res["profit_pct"] > 0.0)
        self.assertTrue(res["final"] > 1000.0)

    def test_non_profitable_path(self):
        # Path A: USDT -> BTC -> ETH -> USDT
        # Step 1: Buy BTC. Recv = (1000 / 60000) * 0.999 = 0.01665 BTC
        # Step 2: Buy ETH. Recv = (0.01665 / 0.050) * 0.999 = 0.33266 ETH
        # Step 3: Sell ETH. Recv = (0.33266 * 2980) * 0.999 = 990.35 USDT
        # Yield should be negative (~-0.96%)
        res = self.detector.check_path_a(1000.0)
        
        self.assertFalse(res["is_profitable"])
        self.assertTrue(res["profit_pct"] < 0.0)

if __name__ == "__main__":
    unittest.main()
