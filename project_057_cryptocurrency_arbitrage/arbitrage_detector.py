"""
Triangular Cryptocurrency Exchange Arbitrage Detector
Author: Portfolio Creator
Description: Models exchange order books as directed graphs, calculates fee-adjusted
             circular trading yields, and flags profitable arbitrage loops.
Language: English (100%)
"""

import os
import json

class ArbitrageDetector:
    """Detects profitable circular trading paths from multi-asset order books."""
    
    def __init__(self, data_path: str, trading_fee: float = 0.001):
        self.data_path = data_path
        self.fee = trading_fee  # Trading fee (0.001 = 0.1%)
        self.rates = {}
        self.load_order_books()

    def load_order_books(self):
        """Loads trading pairs ask and bid prices from JSON database."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Order book file not found: {self.data_path}")
            
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.rates = json.load(f)

    def check_path_a(self, capital: float) -> dict:
        """
        Runs Path A: USDT -> BTC -> ETH -> USDT.
        
        Steps:
        1. Buy BTC with USDT: BTC = (Capital / BTC_USDT_Ask) * (1 - fee)
        2. Buy ETH with BTC: ETH = (BTC / ETH_BTC_Ask) * (1 - fee)
        3. Sell ETH for USDT: USDT = (ETH * ETH_USDT_Bid) * (1 - fee)
        """
        # Step 1: USDT -> BTC
        rate_1 = self.rates["BTC_USDT"]["ask"]
        btc = (capital / rate_1) * (1.0 - self.fee)
        
        # Step 2: BTC -> ETH
        rate_2 = self.rates["ETH_BTC"]["ask"]
        eth = (btc / rate_2) * (1.0 - self.fee)
        
        # Step 3: ETH -> USDT
        rate_3 = self.rates["ETH_USDT"]["bid"]
        usdt_final = (eth * rate_3) * (1.0 - self.fee)
        
        profit_pct = ((usdt_final - capital) / capital) * 100.0
        
        return {
            "path": "USDT -> BTC -> ETH -> USDT",
            "steps": [
                f"1. Buy BTC: Pay {capital:.2f} USDT @ {rate_1:.2f} -> Recv {btc:.6f} BTC",
                f"2. Buy ETH: Pay {btc:.6f} BTC @ {rate_2:.4f} -> Recv {eth:.6f} ETH",
                f"3. Sell ETH: Pay {eth:.6f} ETH @ {rate_3:.2f} -> Recv {usdt_final:.2f} USDT"
            ],
            "initial": capital,
            "final": usdt_final,
            "profit_pct": profit_pct,
            "is_profitable": profit_pct > 0.0
        }

    def check_path_b(self, capital: float) -> dict:
        """
        Runs Path B: USDT -> ETH -> BTC -> USDT.
        
        Steps:
        1. Buy ETH with USDT: ETH = (Capital / ETH_USDT_Ask) * (1 - fee)
        2. Sell ETH for BTC: BTC = (ETH * ETH_BTC_Bid) * (1 - fee)
        3. Sell BTC for USDT: USDT = (BTC * BTC_USDT_Bid) * (1 - fee)
        """
        # Step 1: USDT -> ETH
        rate_1 = self.rates["ETH_USDT"]["ask"]
        eth = (capital / rate_1) * (1.0 - self.fee)
        
        # Step 2: ETH -> BTC
        rate_2 = self.rates["ETH_BTC"]["bid"]
        btc = (eth * rate_2) * (1.0 - self.fee)
        
        # Step 3: BTC -> USDT
        rate_3 = self.rates["BTC_USDT"]["bid"]
        usdt_final = (btc * rate_3) * (1.0 - self.fee)
        
        profit_pct = ((usdt_final - capital) / capital) * 100.0
        
        return {
            "path": "USDT -> ETH -> BTC -> USDT",
            "steps": [
                f"1. Buy ETH: Pay {capital:.2f} USDT @ {rate_1:.2f} -> Recv {eth:.6f} ETH",
                f"2. Sell ETH: Pay {eth:.6f} ETH @ {rate_2:.4f} -> Recv {btc:.6f} BTC",
                f"3. Sell BTC: Pay {btc:.6f} BTC @ {rate_3:.2f} -> Recv {usdt_final:.2f} USDT"
            ],
            "initial": capital,
            "final": usdt_final,
            "profit_pct": profit_pct,
            "is_profitable": profit_pct > 0.0
        }

    def detect_arbitrage(self, capital: float = 1000.0) -> list:
        """Audits all triangular trade directions and returns a list of results."""
        results = [
            self.check_path_a(capital),
            self.check_path_b(capital)
        ]
        return results
