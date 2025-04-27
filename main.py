from function.data_loader import DataLoader
from function.data_analyzer import DataAnalyzer
from function.report import Report
from function.portfolio import Portfolio
import pandas as pd
from function.backtest import Backtester
from function.performance_analyzer import PerformanceAnalyzer






# Paramètres
tickers = ['AAPL', 'MSFT', 'NVDA', 'META', 'JNJ', 'KO', 'XOM', 'JPM', 'PG']
start_date = '2013-01-01'
end_date = '2024-01-01'

# Importation des données
loader = DataLoader(tickers, start_date, end_date)
data = loader.download_data()

# Analyse des données
analyzer = DataAnalyzer(data)

# Résumé statistique
print(analyzer.describe_data())

# Log-returns
returns = analyzer.log_returns()
print(returns.head())

# Graphique des prix
analyzer.plot_prices()

#stocker le graph en png
report = Report(data)
report.save_plot(lambda: analyzer.plot_prices(), "output/stock_prices.png")
report.save_plot(lambda: analyzer.correlation_matrix(), "output/correlation_matrix.png")
report.save_plot(lambda: analyzer.plot_returns(), "output/returns.png")



# Création du rapport
#report = Report()


# === ROLLING BACKTESTS ===
bt_max = Backtester(returns)
bt_max.run_max_sharpe()
report.save_plot(lambda: bt_max.plot_cumulative("Rolling Max Sharpe"), "output/maxsharpe_perf.png")
report.save_plot(lambda: bt_max.plot_weights("Weights - Max Sharpe"), "output/maxsharpe_weights.png")


bt_min = Backtester(returns)
bt_min.run_min_variance()
report.save_plot(lambda: bt_min.plot_cumulative("Rolling Min Variance"), "output/minvar_perf.png")
report.save_plot(lambda: bt_min.plot_weights("Weights - Min Variance"), "output/minvar_weights.png")

portfolio = Portfolio(returns)
w_equal = portfolio.equally_weighted()
report.save_plot(lambda: Portfolio.plot_cumulative_return(w_equal, returns, "Equal Weighted perf"), "output/equal_perf.png")
report.save_plot(lambda: Portfolio.plot_weights(w_equal, returns.columns.tolist(), "Equal Weights"), "output/equal_weights.png")




## analyse finale
weights, static_perfs = Portfolio.build_static_performances(returns)
analyzer = PerformanceAnalyzer()


analyzer.add_strategy("Equal Weighted", static_perfs["Equal"])
analyzer.add_strategy("Max Sharpe", bt_max.perf_df["Cumulative"])
analyzer.add_strategy("Min Variance", bt_min.perf_df["Cumulative"])


print("== Comparaison globale ==")
print(analyzer.compare_all())

print("\n== Focus COVID 2020 ==")
print(analyzer.compare_covid_period())

report.save_plot(lambda: analyzer.plot_all("Comparaison des performances cumulées"), "output/final_comparaison.png")

