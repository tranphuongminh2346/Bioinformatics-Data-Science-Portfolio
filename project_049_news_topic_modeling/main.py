"""
Topic Modeler CLI
Author: Portfolio Creator
Description: CLI driver to fit NMF models and print topic keyword matrices.
Language: English (100%)
"""

import argparse
import sys
import os

# Add the directory containing this file to sys.path to allow running from any directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from topic_modeler import TopicModeler

def main():
    parser = argparse.ArgumentParser(
        description="NMF Topic Modeler - Extract latent themes from article collections."
    )
    parser.add_argument(
        "-i", "--input",
        default="articles.csv",
        help="Path to input news CSV (default: articles.csv)."
    )
    parser.add_argument(
        "-k", "--topics",
        type=int,
        default=2,
        help="Number of latent topics K (default: 2)."
    )
    parser.add_argument(
        "-n", "--words",
        type=int,
        default=5,
        help="Number of top words per topic (default: 5)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Non-Negative Matrix Factorization (NMF) News Topic Modeler")
    print("=" * 60)
    print(f"[*] Input Data  : {args.input}")
    print(f"[*] Topics K    : {args.topics}")
    print(f"[*] Words/Topic : {args.words}")

    try:
        modeler = TopicModeler(args.input)
        print(f"[+] Loaded {len(modeler.df)} news articles.")
        
        # Fit
        print("[*] Building TF-IDF matrix and fitting NMF decomposition...")
        modeler.fit_topics(n_topics=args.topics)
        
        # Keywords
        print("[*] Extracting top keywords per topic...")
        keywords = modeler.get_topic_keywords(top_n=args.words)
        
        print("\n" + "=" * 60)
        print("Extracted Latent Topics & Keywords")
        print("=" * 60)
        for topic_idx, words in keywords.items():
            print(f"[Topic #{topic_idx}] Keywords: {', '.join(words)}")
            
        # Classify
        print("\n[*] Mapping documents to dominant topics...")
        classes = modeler.classify_documents()
        
        print("\n" + "=" * 60)
        print("Document Topic Classification Report")
        print("=" * 60)
        for i, row in modeler.df.iterrows():
            print(f"[{i+1}] Headline: {row['headline']}")
            print(f"    - Assigned Topic: #{row['dominant_topic']}")
            print(f"    - Excerpt: {row['text'][:60]}...")
            print("-" * 60)
            
    except Exception as e:
        print(f"[-] Topic modeler failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nExecution complete.")

if __name__ == "__main__":
    main()
