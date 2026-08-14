"""
Genome-Wide Association Study (GWAS) Manhattan & Q-Q Plotter
Author: Portfolio Creator
Description: Standardizes chromosome layouts, filters genome-wide significant loci,
             and generates publications quality Manhattan and Q-Q plots.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class GWASPlotter:
    """Manages GWAS association matrices, significance testing, and visualizations."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Loads association results and calculates negative log10 p-values."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"GWAS file not found: {self.data_path}")
            
        self.df = pd.read_csv(self.data_path)
        self.df['neg_log_p'] = -np.log10(self.df['p_value'])
        
        # Sort by chromosome and position
        self.df = self.df.sort_values(['chrom', 'pos']).reset_index(drop=True)

    def get_bonferroni_threshold(self, alpha: float = 0.05) -> float:
        """Calculates Bonferroni significance threshold p-value limit."""
        n_tests = len(self.df)
        return alpha / n_tests if n_tests > 0 else alpha

    def get_significant_variants(self, alpha: float = 0.05) -> pd.DataFrame:
        """Filters variants satisfying the Bonferroni significance threshold."""
        threshold = self.get_bonferroni_threshold(alpha)
        return self.df[self.df['p_value'] <= threshold].copy()

    def plot_manhattan(self, output_path: str, alpha: float = 0.05):
        """Generates a Manhattan plot with alternating chromosome colors."""
        df = self.df.copy()
        
        # Calculate cumulative positions
        # Create a column for X-axis coordinate by adding offsets for each chromosome
        df['x_coord'] = 0.0
        offsets = {}
        curr_offset = 0.0
        
        chromosomes = sorted(df['chrom'].unique())
        tick_positions = []
        tick_labels = []
        
        for chrom in chromosomes:
            chrom_data = df[df['chrom'] == chrom]
            max_pos = chrom_data['pos'].max()
            
            offsets[chrom] = curr_offset
            df.loc[df['chrom'] == chrom, 'x_coord'] = chrom_data['pos'] + curr_offset
            
            # Tick position is the center of the chromosome region
            tick_positions.append(curr_offset + (max_pos / 2.0))
            tick_labels.append(str(chrom))
            
            curr_offset += max_pos + 1e6  # Add 1Mb spacer between chromosomes
            
        # Draw plot
        plt.figure(figsize=(12, 6))
        colors = ['#1e293b', '#0284c7']  # Slate gray and Sky blue
        
        for idx, chrom in enumerate(chromosomes):
            chrom_data = df[df['chrom'] == chrom]
            color = colors[idx % len(colors)]
            plt.scatter(
                chrom_data['x_coord'], chrom_data['neg_log_p'],
                color=color, s=25, alpha=0.8, edgecolors='none'
            )
            
        # Draw Bonferroni threshold line
        thresh_p = self.get_bonferroni_threshold(alpha)
        thresh_log = -np.log10(thresh_p)
        plt.axhline(thresh_log, color='#ef4444', linestyle='--', lw=1.5, label='Bonferroni Threshold')
        
        plt.title("GWAS Association Manhattan Plot", fontsize=12, fontweight='bold')
        plt.xlabel("Chromosome")
        plt.ylabel("-log₁₀(p-value)")
        plt.xticks(tick_positions, tick_labels)
        plt.grid(True, axis='y', linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()

    def plot_qq(self, output_path: str):
        """Generates a Q-Q plot of observed vs expected uniform distributions."""
        n = len(self.df)
        if n == 0:
            return
            
        # Sorted observed -log10 p-values
        observed = sorted(self.df['neg_log_p'].values)
        
        # Expected uniform distribution quantiles: rank / (n + 1)
        expected_p = np.arange(1, n + 1) / (n + 1)
        expected = sorted(-np.log10(expected_p))
        
        plt.figure(figsize=(7, 7))
        plt.scatter(expected, observed, color='#0284c7', s=30, alpha=0.8, edgecolors='k', zorder=5)
        
        # Identity line
        max_val = max(max(expected), max(observed)) + 1.0
        plt.plot([0, max_val], [0, max_val], color='#ef4444', linestyle='--', lw=1.5, label='Expected Uniform')
        
        plt.title("GWAS Association Q-Q Plot", fontsize=11, fontweight='bold')
        plt.xlabel("Expected -log₁₀(p-value)")
        plt.ylabel("Observed -log₁₀(p-value)")
        plt.xlim(0, max(expected) + 0.5)
        plt.ylim(0, max_val)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
