"""
Satellite NDVI Matrix Calculator
Author: Portfolio Creator
Description: Computes spatial matrices of Normalized Difference Vegetation Index (NDVI)
             from Red/NIR spectral bands, classifies land covers, and plots heatmaps.
Language: English (100%)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

class NDVICalculator:
    """Loads satellite spectral bands and calculates Normalized Difference Vegetation Indexes."""
    
    def __init__(self, red_path: str, nir_path: str):
        self.red_path = red_path
        self.nir_path = nir_path
        self.red_matrix = None
        self.nir_matrix = None
        self.ndvi_matrix = None
        self.load_bands()

    def load_bands(self):
        """Loads Red and NIR band matrices from CSV."""
        if not os.path.exists(self.red_path):
            raise FileNotFoundError(f"Red band file not found: {self.red_path}")
        if not os.path.exists(self.nir_path):
            raise FileNotFoundError(f"NIR band file not found: {self.nir_path}")
            
        self.red_matrix = np.loadtxt(self.red_path, delimiter=',')
        self.nir_matrix = np.loadtxt(self.nir_path, delimiter=',')
        
        if self.red_matrix.shape != self.nir_matrix.shape:
            raise ValueError("Red and NIR band matrices must share identical spatial dimensions.")

    def calculate_ndvi(self) -> np.ndarray:
        """
        Calculates NDVI matrix: (NIR - Red) / (NIR + Red).
        Protects against division by zero.
        
        Returns:
            np.ndarray: NDVI matrix.
        """
        denominator = self.nir_matrix + self.red_matrix
        numerator = self.nir_matrix - self.red_matrix
        
        # Prevent division by zero
        # Create zero matrix where denominator is zero, divide elsewhere
        self.ndvi_matrix = np.zeros_like(numerator)
        valid_mask = denominator != 0.0
        self.ndvi_matrix[valid_mask] = numerator[valid_mask] / denominator[valid_mask]
        
        # Clip values to valid range [-1.0, 1.0]
        self.ndvi_matrix = np.clip(self.ndvi_matrix, -1.0, 1.0)
        return self.ndvi_matrix

    def classify_land_cover(self) -> dict:
        """
        Categorizes grid cells by NDVI values.
        
        - Water/Snow: NDVI < 0.0
        - Bare Soil:  0.0 <= NDVI < 0.2
        - Shrub/Grass: 0.2 <= NDVI < 0.5
        - Dense Forest: NDVI >= 0.5
        
        Returns:
            dict: Categories mapped to pixel counts and area percentages.
        """
        if self.ndvi_matrix is None:
            self.calculate_ndvi()
            
        total_pixels = self.ndvi_matrix.size
        
        water = np.sum(self.ndvi_matrix < 0.0)
        soil = np.sum((self.ndvi_matrix >= 0.0) & (self.ndvi_matrix < 0.2))
        shrub = np.sum((self.ndvi_matrix >= 0.2) & (self.ndvi_matrix < 0.5))
        forest = np.sum(self.ndvi_matrix >= 0.5)
        
        categories = {
            "Water/Snow": {"count": int(water), "percent": (water / total_pixels) * 100},
            "Bare Soil": {"count": int(soil), "percent": (soil / total_pixels) * 100},
            "Shrub/Grass": {"count": int(shrub), "percent": (shrub / total_pixels) * 100},
            "Dense Forest": {"count": int(forest), "percent": (forest / total_pixels) * 100}
        }
        return categories

    def plot_ndvi(self, output_path: str):
        """Plots NDVI spatial heatmap using YlGn colormap."""
        if self.ndvi_matrix is None:
            self.calculate_ndvi()
            
        plt.figure(figsize=(8, 6))
        im = plt.imshow(self.ndvi_matrix, cmap='YlGn', vmin=-1.0, vmax=1.0, interpolation='nearest')
        
        plt.colorbar(im, label='NDVI Index Value')
        plt.title("Satellite Normalized Difference Vegetation Index (NDVI) Heatmap", fontsize=11, fontweight='bold')
        plt.xlabel("X Grid Pixel Coordinate")
        plt.ylabel("Y Grid Pixel Coordinate")
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
