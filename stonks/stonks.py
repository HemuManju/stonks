from dashboard.components import SideCar, StockPlot

from data.stocks import StockData

side_car = SideCar()
stock_data = StockData()
stock_plot = StockPlot(side_car, stock_data)
stock_plot.plot()
