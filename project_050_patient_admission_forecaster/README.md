# Hospital Patient Admission Forecaster

A healthcare analytics and time series forecasting pipeline that processes daily hospital emergency room admissions records, executes backtest validations on historical data, fits regularized **ARIMA (Autoregressive Integrated Moving Average)** models, and projects daily admission levels for the upcoming week.

## Features
- **Time Series Preprocessing**: Converts flat CSV records into standard pandas DatetimeIndex timeseries, resolving daily frequencies.
- **ARIMA Modeler**: Fits ARIMA(1, 1, 1) autoregressive forecasting equations using `statsmodels`:
  $$\hat{Y}_t = \mu + \sum_{i=1}^p \phi_i Y_{t-i} + \sum_{j=1}^q \theta_j e_{t-j}$$
- **Backtesting & Evaluation**: Implements historical validation splits (e.g. reserving the last 7 days of historical logs) to evaluate Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).
- **Out-of-sample Forecast Visualizer**: Exports trend charts displaying historical lines aligned with the forecasted horizon.

## Project Structure
- `forecaster.py`: Time series indexing, ARIMA fittings, MAE/RMSE calculations, and matplotlib plotters.
- `main.py`: Command-line interface driver.
- `test_forecaster.py`: Unit test suite verifying frequency alignments and validation error indices.
- `admissions.csv`: Sample historical admissions database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To generate admission forecasts:
```bash
python main.py --input admissions.csv --steps 7 --output admissions_forecast.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_forecaster.py
```
