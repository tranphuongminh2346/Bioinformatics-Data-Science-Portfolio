"""
Unit Tests for LJ Dynamics Simulator
Author: Portfolio Creator
Description: Verify initial coordinate spacing, LJ potentials, Verlet steps, and energy conservation.
Language: English (100%)
"""

import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamics_lj import LJDynamicsSimulator

class TestLJDynamicsSimulator(unittest.TestCase):

    def setUp(self):
        # 2 particles in a box of size 8.0, dt = 0.005
        self.sim = LJDynamicsSimulator(n_particles=2, box_size=8.0, dt=0.005)

    def test_grid_initialization(self):
        self.assertEqual(len(self.sim.positions), 2)
        # Verify particles do not overlap initially
        dist = np.sqrt(np.sum((self.sim.positions[0] - self.sim.positions[1]) ** 2))
        self.assertTrue(dist > 1.5)  # Safe grid distance

    def test_lj_potential_value(self):
        # Place particles at exactly r = 1.0 (sigma)
        # Potential V(r) = 4*epsilon * ( (sigma/r)^12 - (sigma/r)^6 )
        # At r = sigma, (sigma/r) = 1.0 -> V(1) = 4 * (1 - 1) = 0.0
        self.sim.positions = np.array([
            [2.0, 2.0],
            [3.0, 2.0]
        ])
        
        _, pot_e = self.sim.compute_forces()
        self.assertAlmostEqual(pot_e, 0.0)
        
        # Place at r = 2^(1/6) * sigma (equilibrium position, min of potential)
        # r = 1.12246 * sigma
        r_min = (2.0 ** (1.0 / 6.0)) * self.sim.sigma
        self.sim.positions = np.array([
            [2.0, 2.0],
            [2.0 + r_min, 2.0]
        ])
        
        # At r_min, potential is -epsilon = -1.0
        _, pot_e = self.sim.compute_forces()
        self.assertAlmostEqual(pot_e, -1.0, places=5)
        # Force should be close to zero at equilibrium position
        np.testing.assert_allclose(self.sim.forces, 0.0, atol=1e-5)

    def test_energy_conservation(self):
        # Run simulation for 20 steps
        self.sim.run_simulation(steps=20)
        
        # Total energy should be conserved within a small drift tolerance (e.g. 0.01)
        tot_energies = [e[2] for e in self.sim.energies]
        drift = np.max(np.abs(np.array(tot_energies) - tot_energies[0]))
        self.assertTrue(drift < 0.005)

if __name__ == "__main__":
    unittest.main()
