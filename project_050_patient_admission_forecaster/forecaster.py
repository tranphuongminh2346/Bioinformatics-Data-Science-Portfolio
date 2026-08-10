"""
Hospital Patient Admission Time Series Forecaster
Author: Portfolio Creator
Description: Fits ARIMA time series models on emergency room admissions,
             calculates MAE/RMSE validation scores, and plots forecast trends.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

class PatientAdmissionForecaster:
    """ARIMA-based patient emergency admission forecasting framework."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Loads daily admission counts and configures DatetimeIndex."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Admissions file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date').set_index('date')
        
        # Enforce daily frequency
        self.df = self.df.asfreq('D')

    def evaluate_validation(self, order: tuple = (1, 1, 1), val_days: int = 7) -> dict:
        """
        Splits data into train/validation, fits ARIMA, and calculates error scores.
        
        Returns:
            dict: MAE, RMSE validation metrics.
        """
        if len(self.df) < val_days * 2:
            raise ValueError("Dataset too short for validation split.")
            
        train = self.df.iloc[:-val_days]
        val = self.df.iloc[-val_days:]
        
        # Fit ARIMA model on train set
        # Suppress warnings for cleaner logs
        model = ARIMA(train['admissions'], order=order)
        model_fit = model.fit()
        
        # Forecast
        forecast = model_fit.forecast(steps=val_days)
        
        mae = mean_absolute_error(val['admissions'], forecast)
        rmse = root_mean_squared_error(val['admissions'], forecast)
        
        return {
            "mae": mae,
            "rmse": rmse,
            "predictions": forecast.values,
            "actuals": val['admissions'].values
        }

    def forecast_future(self, order: tuple = (1, 1, 1), steps: int = 7) -> pd.Series:
        """
        Fits ARIMA model on all historical data and forecasts out-of-sample steps.
        
        Returns:
            pd.Series: Out-of-sample forecasts.
        """
        model = ARIMA(self.df['admissions'], order=order)
        model_fit = model.fit()
        
        forecast = model_fit.forecast(steps=steps)
        return forecast

    def plot_forecast(self, forecast_series: pd.Series, output_path: str):
        """Plots historical admissions alongside out-of-sample forecasted line."""
        plt.figure(figsize=(10, 6))
        
        # Plot historical data
        plt.plot(self.df.index, self.df['admissions'], color='#475569', lw=1.5, label='Historical Admissions')
        
        # Plot forecast
        plt.plot(forecast_series.index, forecast_series.values, color='#0284c7', lw=2, linestyle='--', label='7-Day Forecast')
        
        plt.title("Emergency Room Patient Admissions Time Series Forecast", fontsize=12, fontweight='bold')
        plt.xlabel("Date")
        plt.ylabel("Daily Patient Admissions")
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
