"""
Unit Tests for PHYLIP Parser
Author: Portfolio Creator
Description: Verify PHYLIP headers parsing, base counts, Hamming matrix, and Pi diversity.
Language: English (100%)
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phylip_parser import PhylipParser

class TestPhylipParser(unittest.TestCase):

    def setUp(self):
        # Create a mock PHYLIP file (3 sequences, length 10)
        self.mock_phy = (
            "3 10\n"
            "Seq1      AAAAACCCCC\n"
            "Seq2      AAAAAGGGGG\n"
            "Seq3      TTTTTCCCCC\n"
        )
        
        self.db_fd, self.temp_phy_path = tempfile.mkstemp(suffix=".phy")
        os.close(self.db_fd)
        with open(self.temp_phy_path, 'w', encoding='utf-8') as f:
            f.write(self.mock_phy)
            
        self.parser = PhylipParser(self.temp_phy_path)

    def tearDown(self):
        if os.path.exists(self.temp_phy_path):
            try:
                os.remove(self.temp_phy_path)
            except PermissionError:
                pass

    def test_header_and_records(self):
        self.assertEqual(self.parser.num_seqs, 3)
        self.assertEqual(self.parser.seq_len, 10)
        self.assertIn("Seq1", self.parser.sequences)
        self.assertEqual(self.parser.sequences["Seq1"], "AAAAACCCCC")

    def test_base_composition(self):
        comp = self.parser.get_nucleotide_composition("Seq1")
        
        # 5 As and 5 Cs out of 10 -> 0.5 each
        self.assertAlmostEqual(comp["A"], 0.5)
        self.assertAlmostEqual(comp["C"], 0.5)
        self.assertAlmostEqual(comp["G"], 0.0)

    def test_pairwise_distances(self):
        # Seq1: AAAAACCCCC
        # Seq2: AAAAAGGGGG
        # Difference = 5 sites (all Cs replaced by Gs) -> normalized distance = 5/10 = 0.5
        d_1_2 = self.parser.calculate_pairwise_distance("Seq1", "Seq2")
        self.assertAlmostEqual(d_1_2, 0.5)
        
        # Seq1 vs Seq3 (TTTTTCCCCC) -> 5 differences (all As replaced by Ts) -> 0.5
        d_1_3 = self.parser.calculate_pairwise_distance("Seq1", "Seq3")
        self.assertAlmostEqual(d_1_3, 0.5)
        
        # Seq2 (AAAAAGGGGG) vs Seq3 (TTTTTCCCCC) -> 10 differences -> 1.0
        d_2_3 = self.parser.calculate_pairwise_distance("Seq2", "Seq3")
        self.assertAlmostEqual(d_2_3, 1.0)

    def test_nucleotide_diversity(self):
        # Average distance between all 3 pairs: (0.5 + 0.5 + 1.0) / 3 = 2.0 / 3 = 0.6667
        pi = self.parser.calculate_nucleotide_diversity()
        self.assertAlmostEqual(pi, 2.0 / 3.0)

if __name__ == "__main__":
    unittest.main()
