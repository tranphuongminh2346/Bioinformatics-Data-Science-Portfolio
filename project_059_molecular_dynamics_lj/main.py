"""
LJ Dynamics Simulator CLI
Author: Portfolio Creator
Description: CLI driver to run MD simulations and verify energy conservations.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamics_lj import LJDynamicsSimulator

def main():
    parser = argparse.ArgumentParser(
        description="Lennard-Jones Dynamics Simulator - Run 2D Molecular Dynamics."
    )
    parser.add_argument(
        "-n", "--particles",
        type=int,
        default=4,
        help="Number of particles in box (default: 4)."
    )
    parser.add_argument(
        "-s", "--steps",
        type=int,
        default=100,
        help="Number of integration steps (default: 100)."
    )
    parser.add_argument(
        "-dt", "--dt",
        type=float,
        default=0.01,
        help="Time step size dt (default: 0.01)."
    )
    parser.add_argument(
        "-o", "--output",
        default="dynamics_trajectories.png",
        help="Path to save trajectories plot (default: dynamics_trajectories.png)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("2D Molecular Dynamics Lennard-Jones Simulator")
    print("=" * 60)
    print(f"[*] Particles : {args.particles}")
    print(f"[*] Steps     : {args.steps}")
    print(f"[*] Time step : {args.dt}")
    print(f"[*] Saving to : {args.output}")

    try:
        sim = LJDynamicsSimulator(n_particles=args.particles, dt=args.dt)
        
        print("[*] Running Verlet integration loop...")
        sim.run_simulation(steps=args.steps)
        
        # Display energy conservation
        print("\nEnergy Diagnostics:")
        print(f"    - Initial Total Energy: {sim.energies[0][2]:.6f}")
        print(f"    - Final Total Energy  : {sim.energies[-1][2]:.6f}")
        
        # Calculate maximum fluctuation
        total_energies = [e[2] for e in sim.energies]
        max_fluctuation = np.max(np.abs(np.array(total_energies) - total_energies[0]))
        print(f"    - Max Energy Drift    : {max_fluctuation:.6f} (reduced units)")
        
        # Plot
        print("\n[*] Exporting trajectory diagrams...")
        sim.plot_trajectories(args.output)
        print("[+] Trajectories successfully generated.")
        
    except Exception as e:
        print(f"[-] MD simulation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
