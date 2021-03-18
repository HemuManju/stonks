import streamlit as st
from dashboard.components import SideBar, MainArea

from data.stocks import StockData

# Configuration
st.set_page_config(
    page_title="Stonks",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

stock_data = StockData()
side_bar = SideBar(stock_data)
stock_plot = MainArea(side_bar, stock_data)
stock_plot.plot_history()
stock_plot.plot_technical_indicators()
stock_plot.plot_financials()
