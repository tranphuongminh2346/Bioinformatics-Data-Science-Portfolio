"""
GWAS Plotter CLI
Author: Portfolio Creator
Description: CLI driver to filter significant associations and export Manhattan/Q-Q charts.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gwas_plotter import GWASPlotter

def main():
    parser = argparse.ArgumentParser(
        description="GWAS Plotter - Generate Manhattan and Q-Q plots from association scores."
    )
    parser.add_argument(
        "-i", "--input",
        default="gwas_results.csv",
        help="Path to GWAS results CSV (default: gwas_results.csv)."
    )
    parser.add_argument(
        "-m", "--manhattan",
        default="gwas_manhattan.png",
        help="Path to save Manhattan plot (default: gwas_manhattan.png)."
    )
    parser.add_argument(
        "-q", "--qq",
        default="gwas_qq.png",
        help="Path to save Q-Q plot (default: gwas_qq.png)."
    )
    parser.add_argument(
        "-a", "--alpha",
        type=float,
        default=0.05,
        help="Target alpha significance level for Bonferroni correction (default: 0.05)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("GWAS Manhattan & Q-Q Plotting Pipeline")
    print("=" * 60)
    print(f"[*] Input Data  : {args.input}")
    print(f"[*] Alpha Level : {args.alpha}")

    try:
        plotter = GWASPlotter(args.input)
        print(f"[+] Loaded {len(plotter.df)} genetic variants across {len(plotter.df['chrom'].unique())} chromosomes.")
        
        # Calculate Threshold
        thresh = plotter.get_bonferroni_threshold(args.alpha)
        print(f"[+] Bonferroni corrected threshold P-value limit: {thresh:.3e}")
        
        # Filter significant loci
        print("[*] Auditing genome-wide significant variants...")
        sig_variants = plotter.get_significant_variants(args.alpha)
        
        print("\n" + "=" * 60)
        print("Genome-Wide Significant Loci")
        print("=" * 60)
        print(f"[*] Total Variants: {len(sig_variants)}")
        print("-" * 60)
        for idx, row in sig_variants.iterrows():
            print(f"[{idx+1}] RSID: {row['rsid']:10} | Chrom: {row['chrom']} | Pos: {row['pos']:8} | P-value: {row['p_value']:.2e}")
        print("-" * 60)
        
        # Generate Plots
        print(f"[*] Plotting Manhattan chart to {args.manhattan}...")
        plotter.plot_manhattan(args.manhattan, args.alpha)
        
        print(f"[*] Plotting Q-Q chart to {args.qq}...")
        plotter.plot_qq(args.qq)
        
        print("[+] Visualization plots exported successfully.")
        
    except Exception as e:
        print(f"[-] GWAS plotter failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
