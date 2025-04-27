import yfinance as yf
import pandas as pd

class DataLoader:
    def __init__(self, tickers: list, start: str, end: str):
        self.tickers = tickers
        self.start = start
        self.end = end

    def download_data(self) -> pd.DataFrame:
        data = yf.download(self.tickers, start=self.start, end=self.end)['Close']
        print(data.head())
        return data.dropna() #enlève les NA

    def save_to_csv(self, data: pd.DataFrame, path: str):
        data.to_csv(path)
