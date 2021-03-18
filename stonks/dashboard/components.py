import streamlit as st

from .plots import (candlestick_plot, plot_earnings, plot_technical_indicator,
                    plot_balance)

from get_all_tickers import get_tickers as gt

list_of_tickers = gt.get_tickers()


class SideBar():
    def __init__(self, stock_data):
        self.stock_data = stock_data
        self.ticker_input()
        self.time_input()
        self.technical_analysis_input()

    def ticker_input(self):
        st.sidebar.header('Symbol')
        self.tickers = st.sidebar.multiselect('Type your symbol',
                                              options=list_of_tickers,
                                              default='GME')

    def technical_analysis_input(self):
        st.sidebar.header('Technical Indicators')
        self.volume = st.sidebar.selectbox(
            'Volume',
            options=list(self.stock_data.volume_indicators.keys()),
            key='volume')
        self.volatility = st.sidebar.selectbox(
            'Volatility',
            options=list(self.stock_data.volatility_indicators.keys()),
            key='volatility')
        self.trend = st.sidebar.selectbox(
            'Trend',
            options=list(self.stock_data.trend_indicators.keys()),
            key='trend')
        self.momentum = st.sidebar.selectbox(
            'Momentum',
            options=list(self.stock_data.momentum_indicators.keys()),
            key='momentum')

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
                ],
                                         index=1)


class MainArea():
    def __init__(self, side_bar, stock_data):
        self.side_bar = side_bar
        self.stock_data = stock_data

    def _show_yearnings(self):
        df = self.stock_data.get_earnings()
        df.reset_index(inplace=True)
        fig = plot_earnings(df)
        st.plotly_chart(fig, use_container_width=True)

    def _show_balance(self):
        df = self.stock_data.get_balance()
        fig = plot_balance(df)
        st.plotly_chart(fig, use_container_width=True)

    def _show_stats(self):
        df = self.stock_data.get_summary()
        keys = [
            'averageVolume', 'averageVolume10days', 'beta', 'dayHigh',
            'dayLow', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'forwardPE',
            'fromCurrency', 'lastMarket', 'marketCap', 'maxAge', 'open',
            'payoutRatio', 'previousClose', 'priceHint',
            'priceToSalesTrailing12Months', 'regularMarketDayHigh',
            'regularMarketDayLow', 'regularMarketOpen',
            'regularMarketPreviousClose', 'regularMarketVolume', 'volume'
        ]
        st.dataframe(df.loc[keys, :], height=500)

    def plot_history(self):
        with st.beta_container():
            col1, col2 = st.beta_columns([6, 1])
            with col1:
                st.header('History')
                tickers = self.side_bar.tickers
                period = self.side_bar.period
                interval = self.side_bar.interval

                # Get the data
                df = self.stock_data.get_data(tickers, period, interval)
                fig = candlestick_plot(df)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.header('Trending')
                df = self.stock_data.get_trending()
                st.dataframe(df, height=425)

    def plot_financials(self):
        col1, col2 = st.beta_columns(2)
        with col1:
            st.header('Key Stats')
            self._show_stats()
        with col2:
            st.header('Earnings')
            self._show_yearnings()
            st.header('Balance')
            self._show_balance()

    def show_news(self):
        st.header('News')
        links = self.stock_data.get_news()
        for link in links:
            st.markdown(link)

    def plot_technical_indicators(self):
        df_indicators = self.stock_data.get_technical_analysis()
        st.header('Technical Indicators')
        col1, col2 = st.beta_columns(2)
        with col1:
            # Volume indicator
            key = self.stock_data.volume_indicators[self.side_bar.volume]
            fig = plot_technical_indicator(df_indicators,
                                           key,
                                           title=self.side_bar.volume)
            st.plotly_chart(fig, use_container_width=True)

            # Volatility indicator
            key = self.stock_data.volatility_indicators[
                self.side_bar.volatility]
            fig = plot_technical_indicator(df_indicators,
                                           key,
                                           title=self.side_bar.volatility)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Trend indicator
            key = self.stock_data.trend_indicators[self.side_bar.trend]
            fig = plot_technical_indicator(df_indicators,
                                           key,
                                           title=self.side_bar.trend)
            st.plotly_chart(fig, use_container_width=True)

            # Momentum indicator
            key = self.stock_data.momentum_indicators[self.side_bar.momentum]
            fig = plot_technical_indicator(df_indicators,
                                           key,
                                           title=self.side_bar.momentum)
            st.plotly_chart(fig, use_container_width=True)
