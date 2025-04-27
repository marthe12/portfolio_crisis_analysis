import os
import matplotlib.pyplot as plt
import pandas as pd

class Report:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def save_excel(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.df.to_excel(path)
        print(f"[INFO] Excel report saved to {path}")

    def save_plot(self, plot_func, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.figure()
        plot_func()
        plt.savefig(path)
        print(f"[INFO] Plot saved to {path}")
