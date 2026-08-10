"""
Patient Admission Forecaster CLI
Author: Portfolio Creator
Description: CLI driver to run timeseries forecasts and save trend line plots.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forecaster import PatientAdmissionForecaster

def main():
    parser = argparse.ArgumentParser(
        description="Patient Admission Forecaster - Run ARIMA time series forecasts."
    )
    parser.add_argument(
        "-i", "--input",
        default="admissions.csv",
        help="Path to admissions CSV data (default: admissions.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="admissions_forecast.png",
        help="Path to save forecast plot (default: admissions_forecast.png)."
    )
    parser.add_argument(
        "-s", "--steps",
        type=int,
        default=7,
        help="Number of days to forecast out-of-sample (default: 7)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Hospital Patient Admission Time Series Forecaster")
    print("=" * 60)
    print(f"[*] Input Data  : {args.input}")
    print(f"[*] Forecast   : {args.steps} days")
    print(f"[*] Saving plot : {args.output}")

    try:
        forecaster = PatientAdmissionForecaster(args.input)
        print(f"[+] Loaded {len(forecaster.df)} daily admissions logs.")
        
        # Evaluate model (order = (1, 1, 1) for baseline ARIMA)
        print("[*] Running backtest validation (last 7 days)...")
        metrics = forecaster.evaluate_validation(order=(1, 1, 1), val_days=7)
        print(f"    - Validation MAE : {metrics['mae']:.2f} patients")
        print(f"    - Validation RMSE: {metrics['rmse']:.2f} patients")
        
        # Forecast future
        print(f"[*] Forecasting next {args.steps} days out-of-sample...")
        forecast = forecaster.forecast_future(order=(1, 1, 1), steps=args.steps)
        
        print("\nForecasted Admissions:")
        for date, val in forecast.items():
            print(f"    - {date.strftime('%Y-%m-%d')}: {val:.1f} admissions")
            
        # Plot
        print("\n[*] Exporting timeseries forecast charts...")
        forecaster.plot_forecast(forecast, args.output)
        print("[+] Forecast trend chart successfully exported.")
        
    except Exception as e:
        print(f"[-] Forecaster failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
