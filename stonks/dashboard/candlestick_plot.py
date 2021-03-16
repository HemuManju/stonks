import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, Range1d


def candlestick_plot(df, name):
    # Select the datetime format for the x axis depending on the timeframe
    xaxis_dt_format = '%d %b %Y'
    if df['date'][0].hour > 0:
        xaxis_dt_format = '%d %b %Y, %H:%M:%S'

    fig = figure(sizing_mode='stretch_both',
                 tools="reset, save, box_zoom",
                 active_drag='box_zoom',
                 x_axis_type='linear',
                 x_range=Range1d(df.index[0], df.index[-1], bounds="auto"),
                 title=name,
                 height=350)
    fig.yaxis[0].formatter = NumeralTickFormatter(format="$5.3f")
    inc = df.open > df.close
    dec = ~inc

    # Colour scheme for increasing and descending candles
    INCREASING_COLOR = '#F2583E'
    DECREASING_COLOR = '#49E062'

    width = 0.5
    inc_source = ColumnDataSource(data=dict(x1=df.index[inc],
                                            top1=df.open[inc],
                                            bottom1=df.close[inc],
                                            high1=df.high[inc],
                                            low1=df.low[inc],
                                            Date1=df.date[inc]))

    dec_source = ColumnDataSource(data=dict(x2=df.index[dec],
                                            top2=df.open[dec],
                                            bottom2=df.close[dec],
                                            high2=df.high[dec],
                                            low2=df.low[dec],
                                            Date2=df.date[dec]))
    # Plot candles
    # High and low
    fig.segment(x0='x1',
                y0='high1',
                x1='x1',
                y1='low1',
                source=inc_source,
                line_width=3,
                color=INCREASING_COLOR)
    fig.segment(x0='x2',
                y0='high2',
                x1='x2',
                y1='low2',
                source=dec_source,
                line_width=3,
                color=DECREASING_COLOR)

    # open and close
    r1 = fig.vbar(x='x1',
                  width=width,
                  top='top1',
                  bottom='bottom1',
                  source=inc_source,
                  fill_color=INCREASING_COLOR,
                  line_color="black")
    r2 = fig.vbar(x='x2',
                  width=width,
                  top='top2',
                  bottom='bottom2',
                  source=dec_source,
                  fill_color=DECREASING_COLOR,
                  line_color="black")

    # Add date labels to x axis
    fig.xaxis.major_label_overrides = {
        i: date.strftime(xaxis_dt_format)
        for i, date in enumerate(pd.to_datetime(df['date']))
    }

    # Set up the hover tooltip to display some useful data
    fig.add_tools(
        HoverTool(renderers=[r1],
                  tooltips=[
                      ("open", "$@top1"),
                      ('high', "$@high1"),
                      ('low', "$@low1"),
                      ("close", "$@bottom1"),
                      ('date', "@Date1{" + xaxis_dt_format + "}"),
                  ],
                  formatters={
                      'Date1': 'datetime',
                  }))

    fig.add_tools(
        HoverTool(renderers=[r2],
                  tooltips=[("open", "$@top2"), ('high', "$@high2"),
                            ('low', "$@low2"), ("close", "$@bottom2"),
                            ('date', "@Date2{" + xaxis_dt_format + "}")],
                  formatters={'Date2': 'datetime'}))
    return fig
