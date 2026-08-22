# Backtracking DNA Restriction Mapper

A bioinformatics sequence analysis and algorithmic utility that solves the **Double Digest Problem (DDP)** using a backtracking search algorithm.

Given fragment sizes from single digestions (Enzyme A, Enzyme B) and double digestions (Enzymes A+B), it reconstructs the physical coordinates of restriction sites along the DNA molecule.

## Features
- **Consistency Checks**: Ensures fragment length sums are consistent across all digests.
- **Backtracking Permutation Solver**: Explores fragment order combinations using depth-first search (DFS) permutations and verifies mapped intervals against target double digest fragments.

## Project Structure
- `restriction_mapper.py`: Permutation traversers, coordinate builders, and backtracking solvers.
- `main.py`: Command-line interface driver.
- `test_mapper.py`: Unit test suite verifying length consistency and correct site map coordinates.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To solve Double Digest Problems:
```bash
python main.py -a 2 3 5 -b 1 4 5 -ab 1 1 3 5
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_mapper.py
```
