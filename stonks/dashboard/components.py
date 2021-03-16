import streamlit as st
import pandas as pd

from .candlestick_plot import candlestick_plot


class SideCar():
    def __init__(self):
        self.ticker_input()
        self.time_input()
        self.plot_type_input()

    def ticker_input(self):
        st.sidebar.header('Symbol')
        self.tickers = st.sidebar.multiselect('Type your symbol',
                                              options=['GME', 'AAPL'],
                                              default='GME')

    def plot_type_input(self):
        st.sidebar.header('Plot type')
        self.plot_type = st.sidebar.selectbox(
            'Pick the type', options=['CANDEL STICK', 'TREND'])

    def time_input(self):
        with st.sidebar.beta_container():
            col1, col2 = st.sidebar.beta_columns(2)
            st.header('Time')
            with col1:
                self.period = st.radio('Period', [
                    '1d', '7d', '60d', '1mo', '3mo', '1y', '5y', 'ytd', 'max'
                ])
            with col2:
                self.interval = st.radio('Interval', [
                    '1m', '5m', '30m', '90m', '1d', '5d', '1wk', '1mo', '3mo'
                ])


class StockPlot():
    def __init__(self, side_car, stock_data):
        self.side_car = side_car
        self.stock_data = stock_data

    def plot(self):
        tickers = self.side_car.tickers
        period = self.side_car.period
        interval = self.side_car.interval

        # Get the data
        with st.beta_container():
            for ticker in tickers:
                df = self.stock_data.get_data(tickers, period, interval)
                df.reset_index(inplace=True)
                df["date"] = pd.to_datetime(df["date"],
                                            format='%Y-%m-%d %H:%M:%S')
                fig = candlestick_plot(df, ticker)
                st.bokeh_chart(fig)
