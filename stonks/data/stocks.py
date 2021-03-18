import pandas as pd
import ta
from yahooquery import Ticker
import yahooquery as yq


class StockData():
    def __init__(self):
        self.momentum_indicators = {
            'Relative Strength Index (RSI)': 'momentum_rsi',
            'Rate of Change (ROC)': 'momentum_roc',
        }
        self.volume_indicators = {
            'Money Flow Index (MFI)': 'volume_mfi',
            'Volume Weighted Average Price (VWAP)': 'volume_vwap'
        }
        self.trend_indicators = {
            'Moving Average Convergence Divergence (MACD)': 'trend_macd',
            'KST Oscillator (KST)': 'trend_kst'
        }
        self.volatility_indicators = {
            'Average True Range (ATR)': 'volatility_atr',
            'Ulcer Index (UI)': 'volatility_ui'
        }
        return None

    def get_data(self, ticker, period, interval):
        self.tickers = Ticker(ticker, asynchronous=True)
        self.df = self.tickers.history(period=period, interval=interval)
        self.df.reset_index(inplace=True)
        self.df["date"] = pd.to_datetime(self.df['date'],
                                         format='%Y-%m-%d %H:%M:%S')
        return self.df

    def get_summary(self):
        return pd.DataFrame.from_dict(self.tickers.summary_detail)

    def get_earnings(self):
        df = self.tickers.earning_history
        df['quarter'] = pd.to_datetime(df['quarter'], format='%Y-%m-%d')
        return df

    def get_balance(self):
        df = self.tickers.balance_sheet(frequency='q')
        df.reset_index(inplace=True)
        df = df[['symbol', 'asOfDate', 'TotalAssets', 'TotalDebt']]
        return df

    def get_trending(self):
        data = yq.get_trending()
        items = []
        df = pd.DataFrame()
        for i in range(10):
            items.append(data['quotes'][i]['symbol'])
        df['Symbols'] = items
        return df

    def _make_clickable(self, url, text):
        return f'[{text}]({url})'

    def get_news(self):
        pd.set_option('display.max_colwidth', 400)
        links = []
        news = self.tickers.news(5)
        for item in news:
            links.append(self._make_clickable(item['url'], item['title']))
        return links

    def get_technical_analysis(self):
        df = self.df
        # Drop nans
        df = ta.utils.dropna(df)

        # Add technical indicators
        df_technical = ta.add_all_ta_features(df,
                                              "open",
                                              "high",
                                              "low",
                                              "close",
                                              "volume",
                                              fillna=True)
        return df_technical
