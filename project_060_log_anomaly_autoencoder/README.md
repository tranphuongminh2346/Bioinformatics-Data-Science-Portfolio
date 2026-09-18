# Autoencoder Log Anomaly Detector

A system performance monitoring and data science pipeline that standardizes multi-channel server performance metrics (CPU%, Memory%, Disk I/O, and Network Traffic) and trains an unsupervised **Deep Autoencoder** (implemented using scikit-learn's `MLPRegressor` configured for self-reconstruction $X \to X$) to detect anomalous system states based on reconstruction loss peaks.

## Features
- **Unsupervised Autoencoder Model**: Fits neural networks mapping input features to themselves ($X \to X$) to learn the baseline low-dimensional representation of normal system states.
- **Reconstruction Loss Computations**: Measures row-wise Mean Squared Errors (MSE) between scaled input features and reconstructed outputs:
  $$Loss = \frac{1}{M} \sum_{j=1}^M (X^{scaled}_j - \hat{X}^{scaled}_j)^2$$
- **Motility Diagnostic Thresholds**: Flags logs with reconstruction losses exceeding a configured percentile threshold (e.g. 90th percentile).

## Project Structure
- `autoencoder.py`: Standard Scalers, MLPRegressor auto-associative network trainers, and loss indicators.
- `main.py`: Command-line interface driver.
- `test_autoencoder.py`: Unit test suite verifying scaling outputs and anomaly classifications.
- `server_logs.csv`: Sample hourly server performance database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To audit server logs:
```bash
python main.py --input server_logs.csv --percentile 90.0
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_autoencoder.py
```
