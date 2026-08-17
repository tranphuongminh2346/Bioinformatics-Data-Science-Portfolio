# Triangular Exchange Arbitrage Detector

A cryptocurrency algorithmic trading and data engineering pipeline that parses exchange order books for asset trading pairs (BTC/USDT, ETH/BTC, and ETH/USDT), structures exchange rates as a directed graph accounting for bid/ask spreads, applies transaction fees per swap step, and checks circular trading paths to flag profitable **Triangular Arbitrage** opportunities.

## Features
- **Spread-Aware Conversion Models**: Models buy/sell transactions using ask prices for buys and bid prices for sells.
- **Multi-Step Fee Computations**: Subtracts exchange commission fees (e.g. 0.1% per trade step) sequentially to isolate net yields.
- **Circular Arbitrage Audits**: Evaluates two directions of the triangular cycle:
  - Path A: $USDT \to BTC \to ETH \to USDT$
  - Path B: $USDT \to ETH \to BTC \to USDT$

## Project Structure
- `arbitrage_detector.py`: Graph-rate maps, path calculators, and loop yields checkers.
- `main.py`: Command-line interface driver.
- `test_arbitrage.py`: Unit test suite verifying conversion math and fee subtractions.
- `order_books.json`: Sample exchange order book database.
- `requirements.txt`: Package dependencies.

## Installation
No third-party packages are required. Standard Python library packages are sufficient.
```bash
pip install -r requirements.txt
```

## Usage
To search for exchange arbitrage loops:
```bash
python main.py --input order_books.json --capital 1000 --fee 0.001
```

## Running Unit Tests
To run tests:
```bash
python -m unittest test_arbitrage.py
```
