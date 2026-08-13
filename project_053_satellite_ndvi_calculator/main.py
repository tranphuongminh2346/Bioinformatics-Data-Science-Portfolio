"""
NDVI Calculator CLI
Author: Portfolio Creator
Description: CLI driver to parse band files, print area percentages, and export heatmaps.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ndvi_calculator import NDVICalculator

def main():
    parser = argparse.ArgumentParser(
        description="NDVI Calculator - Compute Normalized Difference Vegetation Index from band matrices."
    )
    parser.add_argument(
        "-r", "--red",
        default="red_band.csv",
        help="Path to Red band CSV matrix (default: red_band.csv)."
    )
    parser.add_argument(
        "-n", "--nir",
        default="nir_band.csv",
        help="Path to NIR band CSV matrix (default: nir_band.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="ndvi_heatmap.png",
        help="Path to save output heatmap (default: ndvi_heatmap.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Satellite NDVI Matrix Calculator & Classification Pipeline")
    print("=" * 60)
    print(f"[*] Red Band : {args.red}")
    print(f"[*] NIR Band : {args.nir}")
    print(f"[*] Heatmap  : {args.output}")

    try:
        calculator = NDVICalculator(args.red, args.nir)
        print(f"[+] Loaded bands with spatial grid dimensions: {calculator.red_matrix.shape}")
        
        # Calculate
        print("[*] Computing Normalized Difference Vegetation Index values...")
        calculator.calculate_ndvi()
        
        # Classify
        print("[*] Performing land cover classification analytics...")
        categories = calculator.classify_land_cover()
        
        print("\n" + "=" * 60)
        print("Land Cover Classification Summary")
        print("=" * 60)
        for cat, data in categories.items():
            print(f"    - {cat:15}: {data['count']:4} pixels ({data['percent']:.1f}%)")
        print("-" * 60)
        
        # Plot
        print("[*] Generating spatial NDVI heatmap plot...")
        calculator.plot_ndvi(args.output)
        print("[+] NDVI heatmap exported successfully.")
        
    except Exception as e:
        print(f"[-] NDVI calculation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
