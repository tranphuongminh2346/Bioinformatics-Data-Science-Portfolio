"""
Autoencoder Log Anomaly CLI
Author: Portfolio Creator
Description: CLI driver to fit neural autoencoders and print flagged logs.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from autoencoder import LogAutoencoder

def main():
    parser = argparse.ArgumentParser(
        description="Autoencoder Log Anomaly Detector - Train MLP network to flag anomalous log entries."
    )
    parser.add_argument(
        "-i", "--input",
        default="server_logs.csv",
        help="Path to input logs CSV (default: server_logs.csv)."
    )
    parser.add_argument(
        "-p", "--percentile",
        type=float,
        default=90.0,
        help="Percentile threshold for anomaly classification (default: 90.0)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Neural Autoencoder Server Log Anomaly Detector")
    print("=" * 60)
    print(f"[*] Input Data  : {args.input}")
    print(f"[*] Percentile  : {args.percentile}%")

    try:
        detector = LogAutoencoder(args.input)
        print(f"[+] Loaded {len(detector.df)} server metrics logs.")
        
        # Train
        print("[*] Training MLP neural network autoencoder (mapping X -> X)...")
        detector.train_autoencoder()
        
        # Losses
        print("[*] Computing reconstruction losses...")
        detector.calculate_reconstruction_errors()
        
        # Flag
        print(f"[*] Flagging anomalies above {args.percentile}th percentile...")
        anomalies = detector.flag_anomalies(threshold_percentile=args.percentile)
        
        print("\n" + "=" * 60)
        print("Flagged Log Anomalies Report")
        print("=" * 60)
        print(f"[*] Total Anomalies Found: {len(anomalies)}")
        print("-" * 60)
        for idx, row in anomalies.iterrows():
            print(f"[Hour Row #{idx:2}] Loss: {row['reconstruction_loss']:.4f}")
            print(f"    - CPU   : {row['cpu_pct']}%")
            print(f"    - Memory: {row['memory_pct']}%")
            print(f"    - DiskIO: {row['disk_io']}")
            print(f"    - Net   : {row['network_traffic']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] Autoencoder pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
