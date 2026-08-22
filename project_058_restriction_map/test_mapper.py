"""
Unit Tests for Restriction Mapper
Author: Portfolio Creator
Description: Verify DDP consistency checks, backtracking solvers, and coordinates maps.
Language: English (100%)
"""

import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from restriction_mapper import RestrictionMapper

class TestRestrictionMapper(unittest.TestCase):

    def setUp(self):
        # Setup input datasets:
        # A: [2, 8] -> Sites A: 0, 2, 10
        # B: [5, 5] -> Sites B: 0, 5, 10
        # AB: [2, 3, 5] -> Sites AB: 0, 2, 5, 10
        self.mapper = RestrictionMapper([2, 8], [5, 5], [2, 3, 5])

    def test_inconsistent_lengths(self):
        # Sum of A = 10, Sum of B = 10, Sum of AB = 11 -> Should raise ValueError
        with self.assertRaises(ValueError):
            RestrictionMapper([2, 8], [5, 5], [2, 3, 6])

    def test_ddp_solutions(self):
        solutions = self.mapper.solve()
        
        # Verify that we find solutions
        self.assertTrue(len(solutions) >= 1)
        
        # A solution should match the known map coordinates:
        # Enzyme A sites: [0, 2, 10] or [0, 8, 10]
        # Enzyme B sites: [0, 5, 10]
        # Combined: [0, 2, 5, 10] or [0, 5, 8, 10]
        found_expected = False
        for sol in solutions:
            if sol["enzyme_a_sites"] == [0, 2, 10] and sol["enzyme_b_sites"] == [0, 5, 10]:
                self.assertEqual(sol["double_sites"], [0, 2, 5, 10])
                found_expected = True
                break
                
        self.assertTrue(found_expected)

if __name__ == "__main__":
    unittest.main()
