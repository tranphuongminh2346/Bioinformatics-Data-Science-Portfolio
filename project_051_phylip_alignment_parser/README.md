# PHYLIP Sequence Alignment Parser

A bioinformatics consensus and evolutionary analysis utility that parses multiple sequence alignments formatted in sequential **PHYLIP** structures.

It computes base fractions, derives normalized Hamming pairwise distance matrices, and calculates nucleotide diversity ($\pi$) indicators.

## Features
- **PHYLIP Sequential Parser**: Parses taxonomy names and aligned characters from standard headers.
- **Pairwise Distance Calculators**: Generates a distance matrix using normalized Hamming distance metrics.
- **Nucleotide Diversity ($\pi$)**: Measures the average degree of polymorphism within the alignment group:
  $$\pi = \frac{2}{N(N-1)} \sum_{i < j} d(i, j)$$

## Project Structure
- `phylip_parser.py`: PHYLIP sequential format parsers, Hamming distance calculators, and diversity estimators.
- `main.py`: Command-line interface driver.
- `test_parser.py`: Unit test suite verifying parsed structures and diversity math.
- `alignment.phy`: Sample PHYLIP alignment database.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To evaluate genetic diversity:
```bash
python main.py --input alignment.phy
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_parser.py
```
