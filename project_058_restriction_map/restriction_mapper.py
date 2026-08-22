"""
Backtracking DNA Restriction Mapper (Double Digest Solver)
Author: Portfolio Creator
Description: Reconstructs physical DNA restriction maps from single and double digests
             using backtracking depth-first search permutations.
Language: English (100%)
"""

import itertools

class RestrictionMapper:
    """Solves the Double Digest Problem (DDP) to reconstruct restriction site coordinates."""
    
    def __init__(self, fragments_a: list, fragments_b: list, fragments_ab: list):
        self.frag_a = fragments_a
        self.frag_b = fragments_b
        self.frag_ab = sorted(fragments_ab)
        
        # Total DNA length must be consistent
        self.length = sum(fragments_ab)
        if sum(fragments_a) != self.length or sum(fragments_b) != self.length:
            raise ValueError("Inconsistent fragment sizes: sum(A) != sum(B) != sum(AB)")

    def solve(self) -> list:
        """
        Runs backtracking search over fragment permutations to find valid site maps.
        
        Returns:
            list: List of dicts representing valid maps (Sites A, Sites B, combined double sites).
        """
        solutions = []
        seen_solutions = set()
        
        # Generate all permutations of fragment orderings for A and B
        # (Using set to avoid duplicates if fragments have identical lengths)
        perms_a = set(itertools.permutations(self.frag_a))
        perms_b = set(itertools.permutations(self.frag_b))
        
        for order_a in perms_a:
            # Reconstruct coordinates for Enzyme A sites
            # e.g. fragment order [2, 3, 5] -> sites: 0, 2, 5, 10
            sites_a = [0]
            curr = 0
            for f in order_a:
                curr += f
                sites_a.append(curr)
                
            for order_b in perms_b:
                # Reconstruct coordinates for Enzyme B sites
                sites_b = [0]
                curr = 0
                for f in order_b:
                    curr += f
                    sites_b.append(curr)
                    
                # Combine sites
                combined_sites = sorted(list(set(sites_a + sites_b)))
                
                # Compute double digest fragments
                calc_ab = []
                for i in range(1, len(combined_sites)):
                    calc_ab.append(combined_sites[i] - combined_sites[i-1])
                    
                # Compare sorted calculated double digest with target
                if sorted(calc_ab) == self.frag_ab:
                    # Found a valid configuration!
                    # Normalize representation to check duplicates (using tuple of tuples)
                    sol_key = (tuple(sites_a), tuple(sites_b))
                    if sol_key not in seen_solutions:
                        seen_solutions.add(sol_key)
                        solutions.append({
                            "enzyme_a_sites": sites_a,
                            "enzyme_b_sites": sites_b,
                            "double_sites": combined_sites
                        })
                        
        return solutions
