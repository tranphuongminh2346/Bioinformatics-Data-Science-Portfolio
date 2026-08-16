# EEG Brainwave Band Power FFT Extractor

A neuroscience signal processing and data engineering pipeline that parses raw single-channel Electroencephalography (EEG) voltage time-series data, applies Fast Fourier Transforms (FFT) to compute the **Power Spectral Density (PSD)**, and integrates frequencies across standard bands (**Delta, Theta, Alpha, Beta, Gamma**) using numerical trapezoidal calculations to report relative brainwave energy distributions.

## Features
- **Power Spectral Density (PSD) Estimator**: Applies Real FFTs on detrended voltage timeseries, mapping raw signals to the frequency domain:
  $$PSD(f) = \frac{|X(f)|^2}{N \cdot f_s}$$
- **Numerical Integration Band Estimator**: Integrates spectral density areas using trapezoidal approximations across standard EEG frequency limits:
  - Delta: 0.5 - 4.0 Hz (deep sleep)
  - Theta: 4.0 - 8.0 Hz (drowsiness)
  - Alpha: 8.0 - 12.0 Hz (relaxed wakefulness)
  - Beta: 12.0 - 30.0 Hz (active thinking)
  - Gamma: 30.0 - 45.0 Hz (cognitive processing)
- **Time/Frequency Multi-Panel Plotter**: Plots raw time domain voltage signals aligned with frequency band power segments.

## Project Structure
- `eeg_extractor.py`: Real FFT calculations, numerical integration bands, detrending steps, and plots.
- `main.py`: Command-line interface driver.
- `test_eeg.py`: Unit test suite verifying frequency bins and peak spectral allocations.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To analyze EEG frequency bands:
```bash
python main.py --input eeg_signal.csv --samplingrate 100.0 --output eeg_spectrum.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_eeg.py
```
