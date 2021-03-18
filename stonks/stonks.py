import streamlit as st
from dashboard.components import SideCar, MainArea

from data.stocks import StockData

# Configuration
st.set_page_config(
    page_title="Stonks",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

stock_data = StockData()
side_car = SideCar(stock_data)
stock_plot = MainArea(side_car, stock_data)
stock_plot.plot_history()
stock_plot.plot_technical_indicators()
stock_plot.plot_financials()
