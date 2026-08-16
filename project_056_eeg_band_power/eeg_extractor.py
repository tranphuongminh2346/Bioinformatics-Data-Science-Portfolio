"""
EEG Brainwave Frequency Band Power Extractor
Author: Portfolio Creator
Description: Standardizes EEG voltage timeseries, applies Fast Fourier Transforms (FFT)
             to compute Power Spectral Density (PSD), and calculates relative band powers.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class EEGBandPowerExtractor:
    """Extracts power spectral density parameters from raw single-channel EEG signals."""
    
    def __init__(self, data_path: str, fs: float = 100.0):
        self.data_path = data_path
        self.fs = fs  # Sampling rate (Hz)
        self.df = None
        self.timestamps = None
        self.voltage = None
        
        self.freqs = None
        self.psd = None
        self.bands = {
            "Delta": (0.5, 4.0),
            "Theta": (4.0, 8.0),
            "Alpha": (8.0, 12.0),
            "Beta": (12.0, 30.0),
            "Gamma": (30.0, 45.0)
        }
        self.load_data()

    def generate_mock_data(self):
        """Generates mock EEG dataset combining Alpha (10Hz) and Beta (20Hz) waves."""
        t = np.arange(0.0, 2.0, 1.0 / self.fs)  # 2 seconds at 100Hz -> 200 samples
        # Alpha: 10 Hz, amp = 15. Beta: 20 Hz, amp = 5.
        alpha_wave = 15.0 * np.sin(2.0 * np.pi * 10.0 * t)
        beta_wave = 5.0 * np.sin(2.0 * np.pi * 20.0 * t)
        np.random.seed(42)
        noise = np.random.normal(0, 2.0, len(t))
        voltage = alpha_wave + beta_wave + noise
        
        df = pd.DataFrame({"timestamp": t, "voltage": voltage})
        df.to_csv(self.data_path, index=False)

    def load_data(self):
        """Loads timestamp and voltage channels from CSV."""
        if not os.path.exists(self.data_path):
            self.generate_mock_data()
            
        self.df = pd.read_csv(self.data_path)
        self.timestamps = self.df['timestamp'].values
        self.voltage = self.df['voltage'].values

    def compute_psd(self) -> tuple:
        """
        Applies standard Real FFT (rfft) to compute Power Spectral Density (PSD).
        
        Returns:
            tuple: (frequencies, power_spectral_density)
        """
        n_samples = len(self.voltage)
        if n_samples == 0:
            return np.array([]), np.array([])
            
        # Detrend signal to remove DC offset (0 Hz component)
        detrended_voltage = self.voltage - np.mean(self.voltage)
        
        # Real FFT
        fft_vals = np.fft.rfft(detrended_voltage)
        self.freqs = np.fft.rfftfreq(n_samples, d=1.0 / self.fs)
        
        # Power Spectral Density (PSD)
        # Scale by sampling frequency to respect Parseval's energy conservation
        self.psd = (np.abs(fft_vals) ** 2) / (n_samples * self.fs)
        
        return self.freqs, self.psd

    def calculate_band_powers(self) -> dict:
        """
        Integrates the power spectral density across standard EEG bands.
        
        Returns:
            dict: Band names mapped to absolute and relative powers.
        """
        if self.psd is None:
            self.compute_psd()
            
        band_powers = {}
        total_power = 0.0
        
        # Calculate absolute powers
        for band_name, (low, high) in self.bands.items():
            mask = (self.freqs >= low) & (self.freqs < high)
            # Area under the PSD curve using trapezoidal numerical integration
            if np.sum(mask) > 1:
                power = np.trapz(self.psd[mask], self.freqs[mask])
            else:
                # Fallback to simple sum if too few points
                power = np.sum(self.psd[mask]) * (self.freqs[1] - self.freqs[0] if len(self.freqs) > 1 else 1.0)
            
            band_powers[band_name] = {"abs_power": power}
            total_power += power
            
        # Calculate relative powers (%)
        for band_name in self.bands:
            abs_p = band_powers[band_name]["abs_power"]
            rel_p = (abs_p / total_power) * 100.0 if total_power > 0 else 0.0
            band_powers[band_name]["rel_power"] = rel_p
            
        return band_powers

    def plot_eeg(self, output_path: str):
        """Plots time domain signal and frequency PSD panels."""
        if self.psd is None:
            self.compute_psd()
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # 1. Time Domain Plot
        ax1.plot(self.timestamps, self.voltage, color='#475569', lw=1)
        ax1.set_title("EEG Time Domain Raw Signal", fontsize=11, fontweight='bold')
        ax1.set_xlabel("Time (seconds)")
        ax1.set_ylabel("Voltage (µV)")
        ax1.grid(True, linestyle=':', alpha=0.5)
        
        # 2. PSD Frequency Domain Plot
        ax2.plot(self.freqs, self.psd, color='#0284c7', lw=1.5)
        ax2.set_title("EEG Power Spectral Density (PSD) using FFT", fontsize=11, fontweight='bold')
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("Power Density (µV²/Hz)")
        ax2.set_xlim(0, 45)  # Truncate at Gamma limit
        ax2.grid(True, linestyle=':', alpha=0.5)
        
        # Shade EEG bands
        colors = {
            "Delta": '#f1f5f9', "Theta": '#e2e8f0', "Alpha": '#cbd5e1',
            "Beta": '#94a3b8', "Gamma": '#64748b'
        }
        for band_name, (low, high) in self.bands.items():
            ax2.axvspan(low, high, color=colors[band_name], alpha=0.3, label=band_name)
            
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
