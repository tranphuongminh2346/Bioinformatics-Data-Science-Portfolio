"""
Unit Tests for News Topic Modeler
Author: Portfolio Creator
Description: Verify TF-IDF dimensions, NMF decomposition shapes, and topic classifications.
Language: English (100%)
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from topic_modeler import TopicModeler

class TestTopicModeler(unittest.TestCase):

    def setUp(self):
        # Create a mock articles dataset of 6 records
        # 3 articles about Space (Mars, rocket, telescope)
        # 3 articles about Finance (rates, stocks, banks)
        self.mock_data = pd.DataFrame({
            "headline": ["H1", "H2", "H3", "H4", "H5", "H6"],
            "text": [
                "Mars rocket telescope launches space",
                "Space rocket launch satellite orbit",
                "Telescope space stars Mars mission",
                "Interest rates federal reserve banks",
                "Stock market prices fall central bank",
                "Rates mortgage banks finance market"
            ]
        })
        
        self.db_fd, self.temp_csv_path = tempfile.mkstemp(suffix=".csv")
        os.close(self.db_fd)
        self.mock_data.to_csv(self.temp_csv_path, index=False)
        self.modeler = TopicModeler(self.temp_csv_path)

    def tearDown(self):
        if os.path.exists(self.temp_csv_path):
            try:
                os.remove(self.temp_csv_path)
            except PermissionError:
                pass

    def test_load(self):
        self.assertEqual(len(self.modeler.df), 6)

    def test_nmf_factorization_shapes(self):
        # Fit K = 2 topics
        W, H = self.modeler.fit_topics(n_topics=2)
        
        # W (document-topic): 6 documents x 2 topics
        self.assertEqual(W.shape, (6, 2))
        
        # H (topic-word): 2 topics x vocabulary size V
        V = self.modeler.tfidf_matrix.shape[1]
        self.assertEqual(H.shape, (2, V))

    def test_document_classification(self):
        self.modeler.fit_topics(n_topics=2)
        classes = self.modeler.classify_documents()
        
        # Verify 6 classes predicted
        self.assertEqual(len(classes), 6)
        
        # The first 3 documents (Space topic) should have the same class
        self.assertEqual(classes[0], classes[1])
        self.assertEqual(classes[1], classes[2])
        
        # The last 3 documents (Finance topic) should have the same class
        self.assertEqual(classes[3], classes[4])
        self.assertEqual(classes[4], classes[5])
        
        # Space topic class should be different from Finance topic class
        self.assertNotEqual(classes[0], classes[3])

if __name__ == "__main__":
    unittest.main()
