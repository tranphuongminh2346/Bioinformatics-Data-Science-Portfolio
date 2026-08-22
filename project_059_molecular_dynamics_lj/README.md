# Lennard-Jones Molecular Dynamics Simulator

A computational physics and biophysics pipeline that simulates a 2D system of interacting gas particles (such as Argon atoms) using the **Lennard-Jones (LJ) potential** and integrates the equations of motion step-by-step using the **Velocity Verlet integration algorithm**.

It monitors kinetic, potential, and total energy parameters at each step to verify the law of conservation of energy.

## Features
- **Lennard-Jones Interactions Model**: Models attractive and repulsive interatomic forces:
  $$V(r) = 4\epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6 \right]$$
  $$F(r) = -\nabla V(r) = \frac{24\epsilon}{r^2} \left[ 2\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6 \right] \mathbf{r}$$
- **Velocity Verlet Integrator**: Solves second-order differential equations of motion:
  $$\mathbf{r}(t+\Delta t) = \mathbf{r}(t) + \mathbf{v}(t)\Delta t + \frac{\mathbf{F}(t)}{2m}\Delta t^2$$
  $$\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \frac{\mathbf{F}(t) + \mathbf{F}(t+\Delta t)}{2m}\Delta t$$
- **Thermodynamic Diagnostics**: Logs total energy drift and plots spatial trajectories.

## Project Structure
- `dynamics_lj.py`: Grid setups, Verlet algorithm updates, LJ force calculations, and trajectory plots.
- `main.py`: Command-line interface driver.
- `test_dynamics.py`: Unit test suite verifying potentials, equilibrium states, and energy drifts.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run molecular simulations:
```bash
python main.py --particles 4 --steps 100 --dt 0.01 --output dynamics_trajectories.png
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_dynamics.py
```
