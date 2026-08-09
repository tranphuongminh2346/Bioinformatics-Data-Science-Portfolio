"""
Unsupervised News Topic Modeler using NMF
Author: Portfolio Creator
Description: Fits Non-Negative Matrix Factorization (NMF) on TF-IDF vectors
             to identify latent themes and classify news articles.
Language: English (100%)
"""

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

class TopicModeler:
    """Decomposes document text matrices to extract latent topics using NMF."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = None
        self.tfidf_matrix = None
        self.W = None  # Document-topic matrix
        self.H = None  # Topic-word matrix
        self.is_fit = False
        self.load_data()

    def load_data(self):
        """Loads headlines and text bodies from CSV."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Articles file not found: {self.data_path}")
        self.df = pd.read_csv(self.data_path)

    def fit_topics(self, n_topics: int = 2) -> tuple:
        """
        Fits TF-IDF vectorizer and NMF topic model.
        
        Returns:
            tuple: (W matrix, H matrix)
        """
        text_data = self.df['text']
        self.tfidf_matrix = self.vectorizer.fit_transform(text_data)
        
        self.model = NMF(n_components=n_topics, init='nndsvd', random_state=42)
        self.W = self.model.fit_transform(self.tfidf_matrix)
        self.H = self.model.components_
        self.is_fit = True
        
        return self.W, self.H

    def get_topic_keywords(self, top_n: int = 5) -> dict:
        """
        Extracts the highest-weighted keywords for each latent topic.
        
        Returns:
            dict: Topic index mapped to list of keyword strings.
        """
        if not self.is_fit:
            raise ValueError("Model must be fit first.")
            
        feature_names = self.vectorizer.get_feature_names_out()
        topic_words = {}
        
        for topic_idx, topic_weights in enumerate(self.H):
            # Sort weights in descending order and select top N feature indexes
            top_word_indices = topic_weights.argsort()[::-1][:top_n]
            topic_words[topic_idx] = [feature_names[i] for i in top_word_indices]
            
        return topic_words

    def classify_documents(self) -> np.ndarray:
        """
        Classifies each document into its most dominant topic.
        
        Returns:
            np.ndarray: Predicted topic indexes for each article.
        """
        if not self.is_fit:
            raise ValueError("Model must be fit first.")
            
        # Argmax across columns of W matrix (document-topic weights)
        dominant_topics = np.argmax(self.W, axis=1)
        self.df['dominant_topic'] = dominant_topics
        return dominant_topics
