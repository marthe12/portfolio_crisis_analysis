import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt


class Portfolio:
    def __init__(self, returns: pd.DataFrame, risk_free_rate: float = 0.01):
        self.returns = returns
        self.mean_returns = returns.mean()*252
        self.cov_matrix = returns.cov()*252
        self.risk_free_rate = risk_free_rate
        self.n_assets = len(returns.columns)

    def equally_weighted(self):
        weights = np.repeat(1 / self.n_assets, self.n_assets)
        return weights

    def min_variance(self):
        def portfolio_variance(weights):
            return weights.T @ self.cov_matrix @ weights

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 0.3) for _ in range(self.n_assets))  # 30% max par actif
        initial_guess = np.repeat(1 / self.n_assets, self.n_assets)

        result = minimize(portfolio_variance, initial_guess, bounds=bounds, constraints=constraints)
        return result.x

    def max_sharpe(self):
        def negative_sharpe_ratio(weights):
            port_return = np.dot(weights, self.mean_returns)
            port_volatility = np.sqrt(weights.T @ self.cov_matrix @ weights)
            return -(port_return - self.risk_free_rate) / port_volatility

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 0.3) for _ in range(self.n_assets))  # 30% max par actif
        initial_guess = np.repeat(1 / self.n_assets, self.n_assets)

        result = minimize(negative_sharpe_ratio, initial_guess, bounds=bounds, constraints=constraints)
        return result.x

    def plot_cumulative_return(weights: np.ndarray, returns: pd.DataFrame,
                               title="Static Portfolio - Cumulative Return"):
        perf = (returns @ weights).to_frame(name="Return")
        perf["Cumulative"] = (1 + perf["Return"]).cumprod()

        perf["Cumulative"].plot(figsize=(12, 6), title=title)
        plt.grid(True)
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.tight_layout()

    @staticmethod
    def plot_weights(weights: np.ndarray, tickers: list, title="Portfolio Weights"):
        plt.figure(figsize=(10, 6))
        plt.bar(tickers, weights)
        plt.title(title)
        plt.ylabel("Weight")
        plt.xticks(rotation=45)
        plt.tight_layout()

    @staticmethod
    def build_static_performances(returns: pd.DataFrame):

        port = Portfolio(returns)
        weights = {
            "Equal": port.equally_weighted(),
            "Min Variance": port.min_variance(),
            "Max Sharpe": port.max_sharpe()
        }

        performances = {}
        for name, w in weights.items():
            perf = (returns @ w).to_frame(name="Return")
            perf["Cumulative"] = (1 + perf["Return"]).cumprod()
            performances[name] = perf["Cumulative"]

        return weights, performances


