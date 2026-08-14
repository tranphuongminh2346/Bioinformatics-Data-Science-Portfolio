# GWAS Manhattan & Q-Q Plotter

A genetics data engineering pipeline that loads Genome-Wide Association Study (GWAS) outputs, filters associated genomic loci using **Bonferroni Multiple-Testing Correction** significance values, and generates publication-grade **Manhattan Plots** (visualizing association coordinates across chromosomes) and **Q-Q Plots** (comparing observed $-\log_{10}(P)$ distributions against expected uniform distributions).

## Features
- **GWAS Data Parser**: Loads chromosome indices, positions, RSIDs, and p-values from CSV tables.
- **Bonferroni Significance Filters**: Dynamically computes statistical thresholds:
  $$P_{threshold} = \frac{\alpha}{N_{tests}}$$
- **Manhattan Plot Visualizer**: Groups variants by chromosome sequentially, alternates colors, and plots negative log p-values.
- **Q-Q Plot Visualizer**: Plots observed vs expected uniform quantiles to evaluate genotyping inflation.

## Project Structure
- `gwas_plotter.py`: Cumulative coordinates offsets, Bonferroni checkers, Manhattan and Q-Q builders.
- `main.py`: Command-line interface driver.
- `test_plotter.py`: Unit test suite verifying log conversions and significance filters.
- `gwas_results.csv`: Sample GWAS association database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To draw association charts:
```bash
python main.py --input gwas_results.csv --manhattan gwas_manhattan.png --qq gwas_qq.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_plotter.py
```
