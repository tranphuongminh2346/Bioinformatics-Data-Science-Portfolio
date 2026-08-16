"""
EEG Extractor CLI
Author: Portfolio Creator
Description: CLI driver to evaluate EEG timeseries and log relative band powers.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from eeg_extractor import EEGBandPowerExtractor

def main():
    parser = argparse.ArgumentParser(
        description="EEG Band Power Extractor - Extract frequency bands using FFT."
    )
    parser.add_argument(
        "-i", "--input",
        default="eeg_signal.csv",
        help="Path to EEG signal CSV data (default: eeg_signal.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="eeg_spectrum.png",
        help="Path to save output chart (default: eeg_spectrum.png)."
    )
    parser.add_argument(
        "-fs", "--samplingrate",
        type=float,
        default=100.0,
        help="EEG sampling frequency in Hz (default: 100.0)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("EEG Brainwave Frequency Band Power Analysis Pipeline")
    print("=" * 60)
    print(f"[*] Input Data  : {args.input}")
    print(f"[*] Sampling Rate: {args.samplingrate} Hz")
    print(f"[*] Saving plot : {args.output}")

    try:
        extractor = EEGBandPowerExtractor(args.input, fs=args.samplingrate)
        print(f"[+] Loaded EEG channel: {len(extractor.voltage)} samples (~{len(extractor.voltage)/args.samplingrate:.1f}s).")
        
        # Compute PSD
        print("[*] Performing Fast Fourier Transform (FFT)...")
        extractor.compute_psd()
        
        # Calculate Bands
        print("[*] Calculating absolute and relative band powers...")
        powers = extractor.calculate_band_powers()
        
        print("\n" + "=" * 60)
        print("EEG Brainwave Frequency Band Report")
        print("=" * 60)
        print("  Band   | Range (Hz) | Absolute Power (µV²) | Relative Power (%)")
        print("-" * 60)
        for band_name, lims in extractor.bands.items():
            p_data = powers[band_name]
            print(f" {band_name:7} | {lims[0]:4.1f}-{lims[1]:4.1f}   | {p_data['abs_power']:20.4f} | {p_data['rel_power']:6.2f}%")
        print("-" * 60)
        
        # Plot
        print("[*] Exporting EEG time and frequency plots...")
        extractor.plot_eeg(args.output)
        print("[+] EEG spectrum plot exported successfully.")
        
    except Exception as e:
        print(f"[-] EEG extraction failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
