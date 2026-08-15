"""
Cell Migration Particle Tracker
Author: Portfolio Creator
Description: Analyzes cell migration coordinates, computes velocities,
             directionality indexes, and Mean Squared Displacements (MSD).
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CellMigrationTracker:
    """Tracks cellular trajectories and extracts physical migration metrics."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.cells = {}  # cell_id -> DataFrame of track coordinates
        self.load_data()

    def load_data(self):
        """Loads tracking coordinates database and groups by cell ID."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Cell tracks file not found: {self.data_path}")
            
        self.df = pd.read_csv(self.data_path)
        self.df = self.df.sort_values(['cell_id', 'frame'])
        
        for cell_id, group in self.df.groupby('cell_id'):
            self.cells[cell_id] = group.reset_index(drop=True)

    def calculate_metrics(self, cell_id: int) -> dict:
        """
        Computes velocity, path lengths, and directionality ratio for a target cell.
        
        Returns:
            dict: Path metrics summary.
        """
        cell_df = self.cells[cell_id]
        x = cell_df['x'].values
        y = cell_df['y'].values
        
        n = len(x)
        if n < 2:
            return {"avg_velocity": 0.0, "total_path": 0.0, "net_displacement": 0.0, "directionality": 0.0}
            
        dx = np.diff(x)
        dy = np.diff(y)
        displacements = np.sqrt(dx ** 2 + dy ** 2)
        
        avg_velocity = np.mean(displacements)
        total_path = np.sum(displacements)
        
        # Net displacement: distance from first to last point
        net_displacement = np.sqrt((x[-1] - x[0]) ** 2 + (y[-1] - y[0]) ** 2)
        
        directionality = net_displacement / total_path if total_path > 0 else 0.0
        
        return {
            "avg_velocity": avg_velocity,
            "total_path": total_path,
            "net_displacement": net_displacement,
            "directionality": directionality
        }

    def calculate_msd(self, cell_id: int, max_lag: int = 5) -> np.ndarray:
        """
        Calculates the Mean Squared Displacement (MSD) for varying lag times.
        
        MSD(tau) = < (x(t+tau) - x(t))^2 + (y(t+tau) - y(t))^2 >
        
        Returns:
            np.ndarray: MSD values indexed by lag time tau (0 to max_lag).
        """
        cell_df = self.cells[cell_id]
        x = cell_df['x'].values
        y = cell_df['y'].values
        n = len(x)
        
        msd = np.zeros(max_lag + 1)
        
        for tau in range(1, max_lag + 1):
            if tau >= n:
                break
            sq_disps = []
            for t in range(n - tau):
                sq_disp = (x[t + tau] - x[t]) ** 2 + (y[t + tau] - y[t]) ** 2
                sq_disps.append(sq_disp)
            msd[tau] = np.mean(sq_disps)
            
        return msd

    def plot_trajectories(self, output_path: str):
        """Plots spatial X-Y trajectories for all cell tracks."""
        plt.figure(figsize=(8, 8))
        
        for cell_id, cell_df in self.cells.items():
            plt.plot(cell_df['x'], cell_df['y'], marker='o', label=f"Cell #{cell_id}", alpha=0.8)
            # Mark starting point
            plt.scatter(cell_df['x'].iloc[0], cell_df['y'].iloc[0], color='green', marker='s', s=40, zorder=5)
            # Mark ending point
            plt.scatter(cell_df['x'].iloc[-1], cell_df['y'].iloc[-1], color='red', marker='x', s=60, zorder=5)
            
        plt.title("Cell Migration Spatial Trajectories Plot", fontsize=12, fontweight='bold')
        plt.xlabel("X Coordinate (µm)")
        plt.ylabel("Y Coordinate (µm)")
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
