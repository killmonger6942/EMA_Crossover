import vectorbt as vbt
import pandas as pd
import numpy as np
from src.data_loader import DataLoader

class VectorBacktester:
    """
    A high-performance vectorized backtester using vectorbt.
    Used for research, parameter optimization, and initial strategy validation.
    """
    
    def __init__(self, ticker: str, start_date: str, end_date: str = None):
        self.ticker = ticker
        loader = DataLoader()
        self.data = loader.get_data(ticker, start_date, end_date)
        
        # Data Cleaning for VectorBT (Handling MultiIndex from yfinance)
        # We only need the 'Close' column for this strategy
        if isinstance(self.data.columns, pd.MultiIndex):
            # If columns are (Price, Ticker), we access 'Close' and then the ticker
            try:
                self.close_price = self.data['Close'][ticker]
            except KeyError:
                # Fallback if structure is slightly different
                self.close_price = self.data.xs('Close', level=0, axis=1)[ticker]
        else:
            self.close_price = self.data['Close']

    def run_single_strategy(self, fast_span: int = 50, slow_span: int = 200):
        """
        Runs a single simulation of the EMA crossover.
        """
        print(f"[INFO] Running Backtest: Fast={fast_span}, Slow={slow_span}")
        
        # 1. Calculate Indicators
        fast_ema = vbt.MA.run(self.close_price, window=fast_span, ewm=True)
        slow_ema = vbt.MA.run(self.close_price, window=slow_span, ewm=True)
        
        # 2. Generate Signals
        # cross_above checks if fast_ema crosses above slow_ema
        entries = fast_ema.ma_crossed_above(slow_ema)
        exits = fast_ema.ma_crossed_below(slow_ema)
        
        # 3. Simulate Portfolio (Assuming $10,000 start, annual fees, slippage)
        portfolio = vbt.Portfolio.from_signals(
            self.close_price,
            entries,
            exits,
            init_cash=10000,
            fees=0.001,      # 0.1% transaction fee
            slippage=0.001,  # 0.1% slippage
            freq='1D'        # Daily data
        )
        
        return portfolio

    def optimize_parameters(self, fast_range: range, slow_range: range):
        """
        Runs a heatmap optimization to find stable parameter clusters.
        """
        print(f"[INFO] Optimizing parameters ({len(fast_range) * len(slow_range)} combinations)...")
        
        # vectorbt allows passing arrays of parameters
        fast_ema = vbt.MA.run(self.close_price, window=fast_range, short_name='fast', ewm=True)
        slow_ema = vbt.MA.run(self.close_price, window=slow_range, short_name='slow', ewm=True)

        entries = fast_ema.ma_crossed_above(slow_ema)
        exits = fast_ema.ma_crossed_below(slow_ema)

        portfolio = vbt.Portfolio.from_signals(
            self.close_price,
            entries,
            exits,
            freq='1D',
            init_cash=10000,
            fees=0.001
        )
        
        return portfolio

if __name__ == "__main__":
    # Initialize
    # We use a long timeframe to ensure we have enough data for a 200-day EMA
    engine = VectorBacktester("SPY", "2010-01-01")
    
    # Run Single Backtest
    pf = engine.run_single_strategy(50, 200)
    
    # Print institutional metrics
    print("\n--- PERFORMANCE METRICS ---")
    print(f"Total Return: {pf.total_return():.2%}")
    print(f"Sharpe Ratio: {pf.sharpe_ratio():.2f}")
    print(f"Max Drawdown: {pf.max_drawdown():.2%}")
    print(f"Win Rate:     {pf.stats()['Win Rate [%]']:.2f}%")
    
    # Optional: Plotting (Uncomment if running in local GUI environment)
    # pf.plot().show()