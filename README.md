# Institutional-Grade EMA Crossover Backtest

## Executive Summary
This project implements an event-driven backtesting engine in Python to audit the performance of the classic Exponential Moving Average (EMA) Crossover strategy against the S&P 500 (SPY). 

Unlike standard retail backtests that rely on in-sample optimization (overfitting), this project utilizes **Walk-Forward Optimization (WFO)** to simulate real-world trading conditions. The research demonstrates that while the strategy generates alpha in trending regimes, it significantly underperforms the benchmark in mean-reverting environments due to "whipsaw" effects, highlighting the necessity for regime-based filtering.

## Key Features
* **Event-Driven Architecture:** Simulates realistic execution with commission modeling (0.2%) and slippage.
* **Walk-Forward Optimization:** Eliminates lookahead bias by re-optimizing parameters (Fast EMA, Slow EMA, Stop Loss) on a rolling 4-year training window.
* **Institutional Risk Metrics:** Integrated `QuantStats` to generate Sharpe Ratio, Sortino Ratio, and Max Drawdown reports.
* **Robustness Validation:** Tested across multiple asset classes (SPY, BTC-USD, NIFTY 50) to verify parameter stability.

## Technical Methodology
The core engine runs on a `Backtesting.py` framework with custom wrapper logic for WFO:
1.  **Data Ingestion:** Fetches Adjusted Close data via `yfinance`.
2.  **Signal Processing:** vector-based calculation of recursive EMAs.
3.  **Risk Management:** Dynamic Trailing Stop loss logic (optimized between 5% - 15%).
4.  **Optimization Loop:** A manual grid-search algorithm designed to be crash-resistant on single-threaded environments.

## Results & Analysis
The Walk-Forward Analysis on SPY (2010–2025) yielded a **Negative Result**, which is a critical finding for risk management:
* **Benchmark (Buy & Hold):** Outperformed the strategy.
* **Strategy Weakness:** The "Golden Cross" (50/200) logic lags significantly during V-shaped recoveries (e.g., Covid 2020), exiting at the bottom and re-entering late.
* **Conclusion:** Simple trend-following is insufficient for efficient markets like the US Large Cap equity space without secondary filters (e.g., Volatility or Regime detection).

## Installation & Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Performance Analysis
![SPY Walk-Forward Analysis](spy_wfo_tearsheet.html)
![Nifty50 Walk-Forward Analysis](nifty_wfo_tearsheet.html)
![BTC Walk-Forward Analysis](crypto_wfo_tearsheet.html)

