import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from function.portfolio import Portfolio

class Backtester:
    def __init__(self, returns: pd.DataFrame, window_size: int = 252*3, test_size: int = 126, step_size: int = 126):
        self.returns = returns
        self.window_size = window_size
        self.test_size = test_size
        self.step_size = step_size
        self.perf_df = None
        self.weights_df = None

    def run_max_sharpe(self):
        weights_list = []
        dates = []
        returns_list = []

        for i in range(0, len(self.returns) - self.window_size - self.test_size, self.step_size):
            window = self.returns.iloc[i : i + self.window_size]
            test_returns = self.returns.iloc[i + self.window_size : i + self.window_size + self.test_size]

            port = Portfolio(window)
            weights = port.max_sharpe()

            daily_returns = test_returns @ weights
            returns_list.extend(daily_returns.tolist())
            dates.extend(test_returns.index.tolist())
            weights_list.extend([weights] * len(daily_returns))

        self.perf_df = pd.DataFrame({
            "Date": dates,
            "Return": returns_list
        }).set_index("Date")

        self.perf_df["Cumulative"] = (1 + self.perf_df["Return"]).cumprod()
        self.weights_df = pd.DataFrame(weights_list, index=dates, columns=self.returns.columns)

    def run_min_variance(self):
        weights_list = []
        dates = []
        returns_list = []

        for i in range(0, len(self.returns) - self.window_size - self.test_size, self.step_size):
            window = self.returns.iloc[i : i + self.window_size]
            test_returns = self.returns.iloc[i + self.window_size : i + self.window_size + self.test_size]

            port = Portfolio(window)
            weights = port.min_variance()

            daily_returns = test_returns @ weights
            returns_list.extend(daily_returns.tolist())
            dates.extend(test_returns.index.tolist())
            weights_list.extend([weights] * len(daily_returns))

        self.perf_df = pd.DataFrame({
            "Date": dates,
            "Return": returns_list
        }).set_index("Date")

        self.perf_df["Cumulative"] = (1 + self.perf_df["Return"]).cumprod()
        self.weights_df = pd.DataFrame(weights_list, index=dates, columns=self.returns.columns)

    def plot_cumulative(self, title="Cumulative Return - Rolling Strategy"):
        if self.perf_df is None:
            raise ValueError("You must run a backtest first.")
        self.perf_df["Cumulative"].plot(figsize=(12, 6), title=title)
        plt.grid(True)
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.tight_layout()

    def plot_weights(self, title="Asset Allocation Over Time"):
        if self.weights_df is None:
            raise ValueError("You must run a backtest first.")
        self.weights_df.plot.area(figsize=(12, 6), title=title)
        plt.ylabel("Weight")
        plt.tight_layout()





