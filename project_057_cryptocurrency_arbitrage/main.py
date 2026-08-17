"""
Arbitrage Detector CLI
Author: Portfolio Creator
Description: CLI driver to evaluate order books and print arbitrage pathways.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from arbitrage_detector import ArbitrageDetector

def main():
    parser = argparse.ArgumentParser(
        description="Arbitrage Detector - Audit circular trading loops on exchange books."
    )
    parser.add_argument(
        "-i", "--input",
        default="order_books.json",
        help="Path to exchange order books JSON (default: order_books.json)."
    )
    parser.add_argument(
        "-c", "--capital",
        type=float,
        default=1000.0,
        help="Initial capital in USDT to simulate trading (default: 1000.0)."
    )
    parser.add_argument(
        "-f", "--fee",
        type=float,
        default=0.001,
        help="Exchange fee per trade step (0.001 = 0.1%%, default: 0.001)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Triangular Exchange Arbitrage Detection Engine")
    print("=" * 60)
    print(f"[*] Input File: {args.input}")
    print(f"[*] Capital   : {args.capital:.2f} USDT")
    print(f"[*] Trade Fee : {args.fee * 100:.2f}% per step")

    try:
        detector = ArbitrageDetector(args.input, trading_fee=args.fee)
        
        print("\n[*] Auditing order book prices...")
        results = detector.detect_arbitrage(capital=args.capital)
        
        print("\n" + "=" * 60)
        print("Triangular Arbitrage Search Report")
        print("=" * 60)
        
        for idx, res in enumerate(results):
            print(f"[Path #{idx+1}] Loop: {res['path']}")
            print("-" * 60)
            for step in res["steps"]:
                print(f"  {step}")
            print("-" * 60)
            status = "PROFITABLE" if res["is_profitable"] else "NON-PROFITABLE"
            print(f"  - Yield Status  : {status}")
            print(f"  - Final Balance : {res['final']:.2f} USDT")
            print(f"  - Yield Return  : {res['profit_pct']:+.4f}%")
            print("=" * 60 + "\n")
            
    except Exception as e:
        print(f"[-] Arbitrage detection failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("Execution complete.")

if __name__ == "__main__":
    main()
