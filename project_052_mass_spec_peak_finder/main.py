"""
MS Peak Finder CLI
Author: Portfolio Creator
Description: CLI driver to run peak detection on mass spectra.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from peak_finder import MassSpecPeakFinder

def main():
    parser = argparse.ArgumentParser(
        description="Mass Spec Peak Finder - Detect peaks and filter by SNR thresholds."
    )
    parser.add_argument(
        "-i", "--input",
        default="mass_spec_signal.csv",
        help="Path to input mass spec CSV (default: mass_spec_signal.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="peaks_detected.png",
        help="Path to save output chart (default: peaks_detected.png)."
    )
    parser.add_argument(
        "-s", "--snr",
        type=float,
        default=3.0,
        help="Minimum Signal-to-Noise Ratio (SNR) threshold (default: 3.0)."
    )
    parser.add_argument(
        "-mh", "--minheight",
        type=float,
        default=200.0,
        help="Minimum peak intensity threshold (default: 200.0)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Mass Spectrometry (MS) Raw Signal Peak Detection Pipeline")
    print("=" * 60)
    print(f"[*] Input Data  : {args.input}")
    print(f"[*] SNR Cutoff  : {args.snr}")
    print(f"[*] Height Cut  : {args.minheight}")
    print(f"[*] Saving plot : {args.output}")

    try:
        finder = MassSpecPeakFinder(args.input)
        print(f"[+] Loaded spectrum with {len(finder.mz)} data points.")
        
        # Run baseline correction
        print("[*] Performing baseline subtraction...")
        finder.remove_baseline()
        
        # Estimate noise
        print("[*] Estimating background noise levels...")
        noise = finder.estimate_noise_std()
        print(f"    - Noise Std Dev: {noise:.4f}")
        
        # Detect
        print("[*] Auditing signal peaks...")
        peaks = finder.detect_peaks(snr_threshold=args.snr, min_height=args.minheight)
        
        print("\n" + "=" * 60)
        print("Detected Mass Spectrometry Peaks Report")
        print("=" * 60)
        print(f"[*] Total Peaks Identified: {len(peaks)}")
        print("-" * 60)
        for idx, p in enumerate(peaks):
            print(f"[{idx+1}] peak Index: {p['index']} | m/z: {p['mz']:.2f} | Raw Int: {p['intensity']:.2f}")
            print(f"    - Corrected Int: {p['corrected_intensity']:.2f} | SNR: {p['snr']:.2f}")
            print("-" * 60)
            
        # Plot
        print("\n[*] Exporting spectrum plots...")
        finder.plot_scan(peaks, args.output)
        print("[+] Spectrum plots successfully generated.")
        
    except Exception as e:
        print(f"[-] Peak finder failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
