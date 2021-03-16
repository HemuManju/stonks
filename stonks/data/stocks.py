import pandas as pd

from yahooquery import Ticker


class StockData():
    def __init__(self):
        return None

    def get_data(self, ticker, period, interval):
        self.tickers = Ticker(ticker, asynchronous=True)
        df = self.tickers.history(period=period, interval=interval)
        return df

    def get_summary(self):
        return pd.DataFrame.from_dict(self.tickers.summary_detail)
