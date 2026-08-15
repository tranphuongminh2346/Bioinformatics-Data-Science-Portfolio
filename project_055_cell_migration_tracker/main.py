"""
Cell Tracker CLI
Author: Portfolio Creator
Description: CLI driver to evaluate cell migration parameters and export trajectory plots.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from particle_tracker import CellMigrationTracker

def main():
    parser = argparse.ArgumentParser(
        description="Cell Migration Tracker - Track spatial cell motility and calculate kinetics."
    )
    parser.add_argument(
        "-i", "--input",
        default="cell_tracks.csv",
        help="Path to cell tracks CSV database (default: cell_tracks.csv)."
    )
    parser.add_argument(
        "-o", "--output",
        default="cell_trajectories.png",
        help="Path to save trajectories plot (default: cell_trajectories.png)."
    )
    parser.add_argument(
        "-l", "--lag",
        type=int,
        default=5,
        help="Maximum lag time interval for MSD calculations (default: 5)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Cell Migration Motility Tracking & Analysis Pipeline")
    print("=" * 60)
    print(f"[*] Input Data  : {args.input}")
    print(f"[*] Max MSD Lag : {args.lag} frames")
    print(f"[*] Saving plot : {args.output}")

    try:
        tracker = CellMigrationTracker(args.input)
        print(f"[+] Loaded tracks database: {len(tracker.df)} rows, {len(tracker.cells)} unique cells.")
        
        # Analyze each cell
        print("\nCell Motility Diagnostics Report:")
        print("-" * 60)
        for cell_id in tracker.cells:
            metrics = tracker.calculate_metrics(cell_id)
            msd = tracker.calculate_msd(cell_id, max_lag=args.lag)
            
            print(f"[Cell #{cell_id}]")
            print(f"    - Avg Velocity    : {metrics['avg_velocity']:.3f} µm/frame")
            print(f"    - Net Displacement: {metrics['net_displacement']:.3f} µm")
            print(f"    - Path Length     : {metrics['total_path']:.3f} µm")
            print(f"    - Directionality  : {metrics['directionality']:.3f}")
            print(f"    - MSD (lag=1..{args.lag}) : {['{:.2f}'.format(x) for x in msd[1:]]}")
            print("-" * 60)
            
        # Plot
        print("[*] Generating trajectories spatial map...")
        tracker.plot_trajectories(args.output)
        print("[+] Motility trajectories plot exported successfully.")
        
    except Exception as e:
        print(f"[-] Cell tracker failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
