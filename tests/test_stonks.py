import streamlit as st
import pandas as pd

from alpha_vantage.timeseries import TimeSeries
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from yahooquery import Ticker


class Test():
    def __init__(self):
        x = st.slider('Select a value')
        st.write(x, 'squared is', x * x)

        st.write("Here's our first attempt at using data to create a table:")
        st.write(
            pd.DataFrame({
                'first column': [1, 2, 3, 4],
                'second column': [10, 20, 30, 40]
            }))

        st.beta_container()
        self.col1, self.col3 = st.beta_columns(2)
        add_selectbox = st.sidebar.selectbox(
            "Symbol", ("Email", "Home phone", "Mobile phone"))
        genre = st.sidebar.radio())

    def run(self):
        with self.col3:
            aapl = Ticker('GME')
            df = pd.DataFrame.from_dict(aapl.summary_detail)
            st.write(df, width=200)

    def run_test(self):
        with self.col1:

            fig = make_subplots(rows=2,
                                cols=1,
                                shared_xaxes=True,
                                vertical_spacing=0.1,
                                subplot_titles=('OHLC', 'Volume'),
                                row_width=[0.4, 0.8])

            # Plot OHLC on 1st row
            fig.add_trace(go.Candlestick(x=df.index,
                                         open=df['1. open'],
                                         high=df['2. high'],
                                         low=df['3. low'],
                                         close=df['4. close'],
                                         name='GME'),
                          row=1,
                          col=1)
            fig.update(layout_xaxis_rangeslider_visible=False)
            # Bar trace for volumes on 2nd row without legend
            fig.add_trace(go.Bar(x=df.index,
                                 y=df['5. volume'],
                                 showlegend=False),
                          row=2,
                          col=1)
            fig.add_hline(y=df['2. high'].values[-1], row=1, col=1)

            fig.layout.template = 'seaborn'
            fig.update(layout_showlegend=False)
            fig.update_layout(hovermode='x',
                              margin=dict(b=20, t=20, l=10, r=10))
            st.write(fig)


test = Test()
test.run()
test.run_test()
