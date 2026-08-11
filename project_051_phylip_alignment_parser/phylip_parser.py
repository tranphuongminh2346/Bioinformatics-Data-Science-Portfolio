"""
PHYLIP Sequence Alignment Parser & Diversity Calculator
Author: Portfolio Creator
Description: Parses sequential PHYLIP multiple sequence alignment files,
             estimates base compositions, and calculates pairwise nucleotide diversities.
Language: English (100%)
"""

import os

class PhylipParser:
    """Parses PHYLIP alignment data and calculates sequence genetics statistics."""
    
    def __init__(self, phy_path: str):
        self.phy_path = phy_path
        self.num_seqs = 0
        self.seq_len = 0
        self.sequences = {}  # Taxon name -> sequence string
        self.load_alignment()

    def load_alignment(self):
        """Parses PHYLIP file structure and stores sequence sequences."""
        if not os.path.exists(self.phy_path):
            raise FileNotFoundError(f"PHYLIP file not found: {self.phy_path}")
            
        with open(self.phy_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            if not lines:
                raise ValueError("Empty PHYLIP file.")
                
            # Parse header: number of sequences and alignment length
            header = lines[0].split()
            if len(header) < 2:
                raise ValueError("Invalid PHYLIP header.")
            self.num_seqs = int(header[0])
            self.seq_len = int(header[1])
            
            # Parse taxa and sequences
            for line in lines[1:self.num_seqs + 1]:
                # PHYLIP standard: Name is first 10 characters (padded with spaces)
                # Some variants separate name and sequence by space, so we accommodate both
                if len(line) <= 10:
                    continue
                name = line[:10].strip()
                seq = line[10:].replace(" ", "").upper()
                self.sequences[name] = seq

    def get_nucleotide_composition(self, name: str) -> dict:
        """
        Calculates fraction of A, C, G, T bases in a sequence.
        
        Returns:
            dict: Base frequencies mapping.
        """
        if name not in self.sequences:
            raise KeyError(f"Taxon '{name}' not found.")
            
        seq = self.sequences[name]
        n = len(seq)
        if n == 0:
            return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "other": 0.0}
            
        comp = {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "other": 0.0}
        for base in seq:
            if base in comp:
                comp[base] += 1
            else:
                comp["other"] += 1
                
        # Normalize
        for k in comp:
            comp[k] /= n
            
        return comp

    def calculate_pairwise_distance(self, name1: str, name2: str) -> float:
        """
        Calculates normalized Hamming distance between two aligned sequences.
        
        Returns:
            float: Fraction of differing sites.
        """
        if name1 not in self.sequences or name2 not in self.sequences:
            raise KeyError("Taxa names not found in alignment.")
            
        s1 = self.sequences[name1]
        s2 = self.sequences[name2]
        
        if len(s1) != len(s2):
            raise ValueError("Aligned sequences must be of identical length.")
            
        diffs = sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)
        return float(diffs) / len(s1) if len(s1) > 0 else 0.0

    def calculate_nucleotide_diversity(self) -> float:
        """
        Computes nucleotide diversity (Pi), the average number of nucleotide differences
        per site between any two sequences:
        
        Pi = [2 / (N * (N - 1))] * Sum_{i < j} d(i, j)
        
        Returns:
            float: Nucleotide diversity score.
        """
        names = list(self.sequences.keys())
        n = len(names)
        if n < 2:
            return 0.0
            
        total_dist = 0.0
        comparison_count = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = self.calculate_pairwise_distance(names[i], names[j])
                total_dist += dist
                comparison_count += 1
                
        return total_dist / comparison_count
