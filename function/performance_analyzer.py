import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PerformanceAnalyzer:
    def __init__(self):
        self.strategies = {}

    def add_strategy(self, name, cumulative_returns: pd.Series):
        self.strategies[name] = cumulative_returns

    def compute_stats(self, series: pd.Series):
        daily_returns = series.pct_change().dropna()
        total_return = series.iloc[-1] - 1   #prend le dernier return (iloc permet d aller chercher dans serie une localisation specifique) et fait -1 -> ex:1.34%-1 = 34% = return tot sur la periode
        volatility = daily_returns.std() * np.sqrt(252)
        sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
        max_drawdown = ((series / series.cummax()) - 1).min()
        return {
            "Total Return": round(total_return, 4),
            "Volatility": round(volatility, 4),
            "Sharpe Ratio": round(sharpe_ratio, 2),
            "Max Drawdown": round(max_drawdown, 4)
        }

    def compare_all(self):
        results = {
            name: self.compute_stats(series)
            for name, series in self.strategies.items()
        }
        return pd.DataFrame(results).T

    def compare_covid_period(self, start="2020-03-01", end="2020-12-31"):
        results = {}
        for name, series in self.strategies.items():
            sub_series = series.loc[start:end]
            if not sub_series.empty:
            #if len(sub_series) > 10:  #pour etre sur d avoir des données (pourrait etre enlevé)
                results[name] = self.compute_stats(sub_series)
        return pd.DataFrame(results).T

    def plot_all(self, title="Cumulative Performance Comparison"):
        plt.figure(figsize=(12,6))
        for name, series in self.strategies.items():
            plt.plot(series, label=name)
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
