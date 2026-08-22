"""
2D Lennard-Jones Molecular Dynamics Simulator using Velocity Verlet Integration
Author: Portfolio Creator
Description: Simulates noble gas particle interactions in 2D using reduced LJ units,
             Velocity Verlet integration, and energy conservation diagnostics.
Language: English (100%)
"""

import numpy as np
import matplotlib.pyplot as plt

class LJDynamicsSimulator:
    """Argon particle Lennard-Jones dynamics engine bounded in a 2D box."""
    
    def __init__(self, n_particles: int = 4, box_size: float = 8.0, dt: float = 0.01,
                 epsilon: float = 1.0, sigma: float = 1.0, mass: float = 1.0):
        self.n = n_particles
        self.box_size = box_size
        self.dt = dt
        self.epsilon = epsilon
        self.sigma = sigma
        self.mass = mass
        self.rc = 2.5 * sigma  # Cutoff radius
        
        # Coordinates matrices: N x 2
        self.positions = None
        self.velocities = None
        self.forces = None
        
        # Diagnostics
        self.trajectory = []  # List of position snapshots
        self.energies = []    # List of (Kinetic, Potential, Total) tuples
        self.initialize_particles()

    def initialize_particles(self):
        """Places particles on a regular grid and assigns random velocities."""
        # Simple grid spacing to avoid overlap
        grid_dim = int(np.ceil(np.sqrt(self.n)))
        xs = np.linspace(2.0, self.box_size - 2.0, grid_dim)
        ys = np.linspace(2.0, self.box_size - 2.0, grid_dim)
        
        coords = []
        for x in xs:
            for y in ys:
                if len(coords) < self.n:
                    coords.append([x, y])
                    
        self.positions = np.array(coords)
        
        # Random velocities with zero net momentum
        np.random.seed(42)
        vels = np.random.normal(0, 0.5, (self.n, 2))
        self.velocities = vels - np.mean(vels, axis=0)
        
        # Initial forces calculation
        self.compute_forces()

    def compute_forces(self) -> tuple:
        """
        Calculates pairwise Lennard-Jones forces and potential energies.
        F(r) = 24*epsilon/r^2 * [ 2*(sigma/r)^12 - (sigma/r)^6 ] * r_vector
        """
        self.forces = np.zeros((self.n, 2))
        pot_energy = 0.0
        
        for i in range(self.n):
            for j in range(i + 1, self.n):
                r_vec = self.positions[i] - self.positions[j]
                r2 = np.sum(r_vec ** 2)
                r = np.sqrt(r2)
                
                if r < self.rc:
                    # Calculate potential energy
                    sr6 = (self.sigma / r) ** 6
                    sr12 = sr6 ** 2
                    v_pair = 4.0 * self.epsilon * (sr12 - sr6)
                    pot_energy += v_pair
                    
                    # Calculate force magnitude
                    f_mag = (24.0 * self.epsilon / r2) * (2.0 * sr12 - sr6)
                    f_vec = f_mag * r_vec
                    
                    # Newton's Third Law
                    self.forces[i] += f_vec
                    self.forces[j] -= f_vec
                    
        return self.forces, pot_energy

    def calculate_kinetic_energy(self) -> float:
        """K = 0.5 * m * sum(v^2)."""
        v2 = np.sum(self.velocities ** 2)
        return 0.5 * self.mass * v2

    def step(self):
        """
        Executes a single step of the Velocity Verlet integration algorithm.
        1. r(t + dt) = r(t) + v(t)dt + F(t)/(2m) * dt^2
        2. Calculate new forces F(t + dt)
        3. v(t + dt) = v(t) + (F(t) + F(t+dt))/(2m) * dt
        """
        # Save snapshot
        self.trajectory.append(self.positions.copy())
        
        # 1. Update positions
        self.positions += self.velocities * self.dt + (self.forces / (2.0 * self.mass)) * (self.dt ** 2)
        
        # Handle simple reflecting boundary walls (bouncing)
        for i in range(self.n):
            for dim in range(2):
                if self.positions[i, dim] < 0.0:
                    self.positions[i, dim] = -self.positions[i, dim]
                    self.velocities[i, dim] = -self.velocities[i, dim]
                elif self.positions[i, dim] > self.box_size:
                    self.positions[i, dim] = 2.0 * self.box_size - self.positions[i, dim]
                    self.velocities[i, dim] = -self.velocities[i, dim]
                    
        # Store old forces
        old_forces = self.forces.copy()
        
        # 2. Compute new forces and potential energy
        _, pot_e = self.compute_forces()
        
        # 3. Update velocities
        self.velocities += ((old_forces + self.forces) / (2.0 * self.mass)) * self.dt
        
        # Save energies
        kin_e = self.calculate_kinetic_energy()
        tot_e = kin_e + pot_e
        self.energies.append((kin_e, pot_e, tot_e))

    def run_simulation(self, steps: int = 100):
        """Runs the Verlet MD loop for a number of steps."""
        for _ in range(steps):
            self.step()

    def plot_trajectories(self, output_path: str):
        """Plots the spatial trajectory paths of all particles in the box."""
        traj_array = np.array(self.trajectory)  # Steps x N x 2
        
        plt.figure(figsize=(8, 8))
        
        for i in range(self.n):
            x_pts = traj_array[:, i, 0]
            y_pts = traj_array[:, i, 1]
            plt.plot(x_pts, y_pts, label=f"Particle #{i}", alpha=0.8)
            plt.scatter(x_pts[0], y_pts[0], color='green', marker='s', s=30)
            plt.scatter(x_pts[-1], y_pts[-1], color='red', marker='o', s=30)
            
        plt.xlim(0, self.box_size)
        plt.ylim(0, self.box_size)
        plt.title("2D Molecular Dynamics Lennard-Jones Trajectories", fontsize=12, fontweight='bold')
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
