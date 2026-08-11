"""
PHYLIP Parser CLI
Author: Portfolio Creator
Description: CLI driver to parse PHYLIP alignments, print compositions, and calculate Pi.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phylip_parser import PhylipParser

def main():
    parser = argparse.ArgumentParser(
        description="PHYLIP Alignment Parser - Analyze genetic multiple sequence alignments."
    )
    parser.add_argument(
        "-i", "--input",
        default="alignment.phy",
        help="Path to input sequential PHYLIP file (default: alignment.phy)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("PHYLIP Sequence Alignment Parser & Diversity Calculator")
    print("=" * 60)
    print(f"[*] Input File: {args.input}")

    try:
        parser_obj = PhylipParser(args.input)
        print(f"[+] Parsed {parser_obj.num_seqs} sequences of length {parser_obj.seq_len} bp.")
        
        # Compositions
        print("\nTaxon Nucleotide Composition:")
        print("-" * 60)
        for name in parser_obj.sequences:
            comp = parser_obj.get_nucleotide_composition(name)
            print(f"    - {name:10} | A: {comp['A']:.2f} | C: {comp['C']:.2f} | G: {comp['G']:.2f} | T: {comp['T']:.2f}")
            
        # Pairwise Distance Matrix
        print("\nPairwise Normalized Distance Matrix:")
        print("-" * 60)
        taxa = sorted(list(parser_obj.sequences.keys()))
        # Print header
        print("          " + " ".join(f"{t[:8]:>8}" for t in taxa))
        for t1 in taxa:
            row_str = []
            for t2 in taxa:
                dist = parser_obj.calculate_pairwise_distance(t1, t2)
                row_str.append(f"{dist:.4f}")
            print(f"{t1[:10]:10} " + " ".join(row_str))
            
        # Nucleotide Diversity
        print("\n" + "=" * 60)
        pi = parser_obj.calculate_nucleotide_diversity()
        print(f"[+] Nucleotide Diversity (Pi): {pi:.6f}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[-] Alignment parser failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
