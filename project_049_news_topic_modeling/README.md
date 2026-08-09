# NMF News Topic Modeler

An unsupervised text mining pipeline that vectorizes documents using TF-IDF, performs **Non-Negative Matrix Factorization (NMF)** to decompose documents into latent themes, extracts topic-defining keywords, and classifies news articles into topics.

## Features
- **TF-IDF Text Vectorization**: Processes text corpora and converts documents into weighted token vectors.
- **NMF Decomposition Matrix Factorization**: Factorizes the document-term matrix $V$ ($D \times W$) into non-negative matrices $W$ ($D \times K$, document-topic representation) and $H$ ($K \times W$, topic-word weights):
  $$V \approx W \times H$$
- **Topic Keyword & Document Classifiers**: Extracts top words from the $H$ matrix and assigns documents to dominant topics using the $W$ matrix.

## Project Structure
- `topic_modeler.py`: Text vectorization, NMF decomposition, keyword extraction, and document classification.
- `main.py`: Command-line interface driver.
- `test_modeler.py`: Unit test suite verifying factorization shapes and class groupings.
- `articles.csv`: Sample news articles database.
- `requirements.txt`: Package dependencies.

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To model news topics:
```bash
python main.py --input articles.csv --topics 2 --words 5
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_modeler.py
```
