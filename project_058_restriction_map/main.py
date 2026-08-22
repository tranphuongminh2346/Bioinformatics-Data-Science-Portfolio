"""
Restriction Mapper CLI
Author: Portfolio Creator
Description: CLI driver to solve DDP instances and display restriction maps.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from restriction_mapper import RestrictionMapper

def main():
    parser = argparse.ArgumentParser(
        description="Double Digest Restriction Mapper - Reconstruct restriction sites from fragment lengths."
    )
    # Default example:
    # A fragments = [2, 3, 5], sum = 10
    # B fragments = [1, 4, 5], sum = 10
    # AB double fragments = [1, 1, 3, 5], sum = 10
    parser.add_argument(
        "-a", "--enzyme_a",
        type=int,
        nargs="+",
        default=[2, 3, 5],
        help="Fragment sizes for Enzyme A (default: 2 3 5)."
    )
    parser.add_argument(
        "-b", "--enzyme_b",
        type=int,
        nargs="+",
        default=[1, 4, 5],
        help="Fragment sizes for Enzyme B (default: 1 4 5)."
    )
    parser.add_argument(
        "-ab", "--double_digest",
        type=int,
        nargs="+",
        default=[1, 1, 3, 5],
        help="Fragment sizes for Double Digest A+B (default: 1 1 3 5)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Double Digest Restriction Mapping Solver (DDP)")
    print("=" * 60)
    print(f"[*] Enzyme A fragments: {args.enzyme_a}")
    print(f"[*] Enzyme B fragments: {args.enzyme_b}")
    print(f"[*] Double fragments  : {args.double_digest}")

    try:
        mapper = RestrictionMapper(args.enzyme_a, args.enzyme_b, args.double_digest)
        print(f"[*] Reconstructing DNA molecules of total length: {mapper.length} bp...")
        
        solutions = mapper.solve()
        
        print("\n" + "=" * 60)
        print("Reconstructed DNA Physical Maps")
        print("=" * 60)
        print(f"[*] Total Valid Maps Found: {len(solutions)}")
        print("-" * 60)
        for idx, sol in enumerate(solutions):
            print(f"[Map Solution #{idx+1}]")
            print(f"    - Enzyme A cut sites (bp): {sol['enzyme_a_sites']}")
            print(f"    - Enzyme B cut sites (bp): {sol['enzyme_b_sites']}")
            print(f"    - Combined cut sites (bp): {sol['double_sites']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] Mapping solver failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
