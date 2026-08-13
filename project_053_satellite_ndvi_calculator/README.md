# Satellite NDVI Matrix Calculator

A remote sensing data engineering pipeline that loads Red and Near-Infrared (NIR) band reflectance matrices from satellite data, calculates the **Normalized Difference Vegetation Index (NDVI)** matrix, handles zero-division coordinates, categorizes land cover distributions, and exports spatial heatmaps.

## Features
- **Spectral Band Matrix Parsers**: Loads 2D spatial grid arrays representing Red and NIR reflectances from CSV.
- **NDVI Calculator**: Calculates vegetation health indices:
  $$NDVI = \frac{NIR - Red}{NIR + Red}$$
  Handles zero-division coordinates safely by masking out pixels where $NIR + Red = 0$.
- **Land Cover Classifier**: Groups pixel arrays into four classifications (Water/Snow, Bare Soil, Shrub/Grass, and Dense Forest).
- **Spatial Heatmap Plotter**: Plots the 2D spatial grid heatmap using green-yellow-brown colormaps to highlight vegetation density.

## Project Structure
- `ndvi_calculator.py`: Band loading, division masks, land category counts, and colormap plotters.
- `main.py`: Command-line interface driver.
- `test_ndvi.py`: Unit test suite verifying grid dimensions, division limits, and classifications.
- `red_band.csv` / `nir_band.csv`: Sample spatial satellite reflectance databases.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To evaluate vegetation health:
```bash
python main.py --red red_band.csv --nir nir_band.csv --output ndvi_heatmap.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_ndvi.py
```
