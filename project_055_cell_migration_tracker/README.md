# Cell Migration Particle Tracker

A biophysics data engineering and analysis pipeline that processes 2D spatial cell migration coordinates, calculates movement velocities, derives **Directionality Indices** (the straightness of migration paths), and computes **Mean Squared Displacements (MSD)** across lag intervals to classify diffusive vs directed cell motility.

It generates trajectory maps visualizing cell tracks with start and end markers.

## Features
- **Motility Metrics Estimator**: Calculates path lengths, net displacements, average velocities, and directionality indices:
  $$D = \frac{d_{net}}{d_{total}}$$
- **Mean Squared Displacement (MSD) Profiler**: Computes MSD across multiple lag steps:
  $$MSD(\tau) = \langle (r(t+\tau) - r(t))^2 \rangle$$
  Enables classification of random walk diffusion vs directed chemotactic motility.
- **Trajectory Visualizer**: Plots spatial coordinates of cell tracks with color-coded trajectories.

## Project Structure
- `particle_tracker.py`: Path displacement estimators, directionality indicators, MSD calculators, and plots.
- `main.py`: Command-line interface driver.
- `test_tracker.py`: Unit test suite verifying displacement velocities and directionality limits.
- `cell_tracks.csv`: Sample spatial cell tracking coordinates database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To evaluate cell motility:
```bash
python main.py --input cell_tracks.csv --output cell_trajectories.png --lag 5
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_tracker.py
```
