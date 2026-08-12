# Mass Spectrometry Peak Finder

A mass spectrometry signal processing and data engineering pipeline that loads raw $m/z$ and intensity data arrays, performs baseline subtraction using rolling median filters, estimates background noise levels, and detects significant mass peaks using customized Signal-to-Noise Ratio (SNR) and height thresholds.

It plots baseline estimations and highlights detected peaks with annotations.

## Features
- **Rolling Median Baseline Subtraction**: Corrects spectrum intensity shifts by subtracting median values over window sizes:
  $$I_{corrected} = \max(0, I_{raw} - \text{median}(I_{raw}))$$
- **Background Noise Estimation**: Evaluates noise standard deviations exclusively on non-peak regions to prevent skewing threshold limits.
- **Significant Peak Detectors**: Identifies local maxima using Scipy's peak finding algorithms and filters output by SNR:
  $$SNR = \frac{I_{corrected}}{\sigma_{noise}} \ge \text{Threshold}$$

## Project Structure
- `peak_finder.py`: Rolling median filters, background noise estimators, peak algorithms, and plots.
- `main.py`: Command-line interface driver.
- `test_peaks.py`: Unit test suite verifying baseline shifts and peak SNR counts.
- `mass_spec_signal.csv`: Sample mass spectrometry scan database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To find mass peaks:
```bash
python main.py --input mass_spec_signal.csv --snr 3.0 --minheight 200.0 --output peaks_detected.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_peaks.py
```
