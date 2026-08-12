"""
Mass Spectrometry (MS) Peak Finder
Author: Portfolio Creator
Description: Subtracts baseline noise, estimates noise standard deviation,
             finds mass peaks, and reports Signal-to-Noise Ratios (SNR).
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

class MassSpecPeakFinder:
    """Finds peaks and evaluates SNRs in mass spectrometry scans."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.mz = None
        self.intensity = None
        
        self.baseline = None
        self.corrected_intensity = None
        self.noise_std = 0.0
        
        self.load_data()

    def load_data(self):
        """Loads m/z and intensity arrays from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Mass spec file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.mz = self.df['mz'].values
        self.intensity = self.df['intensity'].values

    def remove_baseline(self, window_size: int = 15) -> np.ndarray:
        """
        Subtracts rolling median baseline from raw intensity signal.
        
        Returns:
            np.ndarray: Baseline corrected intensity.
        """
        # Pad edges to maintain array length
        pad_width = window_size // 2
        padded = np.pad(self.intensity, pad_width, mode='edge')
        
        # Calculate rolling median
        baseline = []
        for i in range(len(self.intensity)):
            window = padded[i:i + window_size]
            baseline.append(np.median(window))
            
        self.baseline = np.array(baseline)
        self.corrected_intensity = self.intensity - self.baseline
        
        # Clip negative values resulting from noise fluctuations to zero
        self.corrected_intensity = np.clip(self.corrected_intensity, 0, None)
        return self.corrected_intensity

    def estimate_noise_std(self) -> float:
        """
        Estimates the standard deviation of background noise.
        We estimate noise using only points below a cutoff threshold (e.g. < 100)
        to prevent peaks from inflating noise estimates.
        """
        if self.corrected_intensity is None:
            self.remove_baseline()
            
        background_points = self.corrected_intensity[self.intensity < 100.0]
        if len(background_points) < 5:
            # Fallback to full series std
            self.noise_std = np.std(self.corrected_intensity)
        else:
            self.noise_std = np.std(background_points)
            
        # Avoid division by zero
        if self.noise_std == 0:
            self.noise_std = 1.0
            
        return self.noise_std

    def detect_peaks(self, snr_threshold: float = 3.0, min_height: float = 200.0) -> list:
        """
        Detects significant peaks using height thresholds and SNR criteria.
        
        Returns:
            list: List of dicts representing detected peaks (index, m/z, intensity, SNR).
        """
        if self.corrected_intensity is None:
            self.remove_baseline()
        if self.noise_std == 0:
            self.estimate_noise_std()
            
        # Find local maxima using scipy.signal.find_peaks
        peaks_indices, _ = sig.find_peaks(self.corrected_intensity, height=min_height, distance=5)
        
        detected_peaks = []
        for idx in peaks_indices:
            peak_intensity = self.corrected_intensity[idx]
            snr = peak_intensity / self.noise_std
            
            if snr >= snr_threshold:
                detected_peaks.append({
                    "index": idx,
                    "mz": self.mz[idx],
                    "intensity": self.intensity[idx],
                    "corrected_intensity": peak_intensity,
                    "snr": snr
                })
                
        return detected_peaks

    def plot_scan(self, detected_peaks: list, output_path: str):
        """Plots raw spectrum, baseline, and flags peaks."""
        plt.figure(figsize=(10, 6))
        
        # 1. Plot raw spectrum
        plt.plot(self.mz, self.intensity, color='#94a3b8', alpha=0.7, label='Raw Spectrum')
        
        # 2. Plot baseline
        if self.baseline is not None:
            plt.plot(self.mz, self.baseline, color='#ef4444', linestyle=':', label='Estimated Baseline')
            
        # 3. Highlight peaks
        peak_mzs = [p["mz"] for p in detected_peaks]
        peak_ints = [p["intensity"] for p in detected_peaks]
        plt.scatter(peak_mzs, peak_ints, color='#0284c7', s=80, marker='v', zorder=5, label='Detected Peaks')
        
        # Add labels
        for p in detected_peaks:
            plt.annotate(
                f"{p['mz']:.1f}\n(SNR: {p['snr']:.1f})",
                xy=(p["mz"], p["intensity"]),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.5)
            )
            
        plt.title("Mass Spectrometry Raw Signal Peak Detection", fontsize=12, fontweight='bold')
        plt.xlabel("Mass-to-Charge Ratio (m/z)")
        plt.ylabel("Intensity")
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
