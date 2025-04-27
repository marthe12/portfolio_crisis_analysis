import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def describe_data(self):
        return self.data.describe()

    def log_returns(self) -> pd.DataFrame:
        log_ret = np.log(self.data / self.data.shift(1))
        return log_ret.dropna()

    def plot_prices(self):
        self.data.plot(figsize=(12, 6))
        plt.title("Stock Prices Over Time")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.grid(True)
        plt.tight_layout()

    def correlation_matrix(self):
        corr = self.log_returns().corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix of Log Returns")
        plt.tight_layout()

    def plot_returns(self):
        cumulative = (1 + self.log_returns()).cumprod()
        cumulative.plot(figsize=(12, 6))
        plt.title("Cumulative Log Returns")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.grid(True)
        plt.tight_layout()





