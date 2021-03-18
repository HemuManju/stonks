import plotly.graph_objects as go
from plotly.subplots import make_subplots


def update_fig_style(fig):
    fig.update_layout(template='plotly_white',
                      xaxis=dict(ticks="outside", mirror=True, showline=True),
                      yaxis=dict(ticks="outside", mirror=True, showline=True),
                      margin=dict(l=0, r=0, t=20, b=0))
    fig.update_xaxes(mirror=True)
    fig.update_layout(showlegend=True)
    return fig


def plot_balance(df):
    fig = go.Figure()
    dfs = [x for _, x in df.groupby(df['symbol'])]
    for df in dfs:
        fig.add_trace(
            go.Bar(name='Asst ' + df['symbol'].values[0],
                   x=df['asOfDate'],
                   y=df['TotalAssets']))
        fig.add_trace(
            go.Bar(name='Debt ' + df['symbol'].values[0],
                   x=df['asOfDate'],
                   y=df['TotalDebt']))

        # Change the bar mode
        fig.update_layout(barmode='group')
        fig = update_fig_style((fig))

        fig.update_layout(height=200)
    return fig


def plot_technical_indicator(df, indicator, title='Title'):
    fig = go.Figure()
    dfs = [x for _, x in df.groupby(df['symbol'])]
    for df in dfs:
        fig.add_trace(
            go.Scatter(name=df['symbol'].values[0],
                       x=df['date'],
                       y=df[indicator],
                       mode='lines'))
        fig = update_fig_style(fig)
        fig.update_layout(title=title, margin=dict(l=0, r=0, t=25, b=0))
        fig.update_layout(height=175)

    return fig


def plot_earnings(df):
    fig = go.Figure()
    dfs = [x for _, x in df.groupby(df['symbol'])]
    for df in dfs:
        fig.add_trace(
            go.Scatter(x=df['quarter'],
                       y=df['epsActual'].values,
                       marker=dict(size=15),
                       name='Act. ' + df['symbol'].values[0]))
        fig.add_trace(
            go.Scatter(x=df['quarter'],
                       y=df['epsEstimate'],
                       marker=dict(size=15),
                       name='Est. ' + df['symbol'].values[0]))
        fig = update_fig_style(fig)
        fig.update_layout(height=200)

    return fig


def candlestick_plot(df):
    fig = make_subplots(rows=2,
                        cols=1,
                        vertical_spacing=0.125,
                        subplot_titles=('OHLC', 'Volume'),
                        row_width=[0.3, 0.7])
    dfs = [x for _, x in df.groupby(df['symbol'])]
    for df in dfs:
        fig.add_trace(go.Candlestick(x=df['date'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close'],
                                     increasing_line_color='#DD5E56',
                                     decreasing_line_color='#51A39A',
                                     name=df['symbol'].values[0]),
                      row=1,
                      col=1)
        fig.add_trace(go.Bar(name=df['symbol'].values[0],
                             x=df['date'],
                             y=df['volume'],
                             showlegend=False),
                      row=2,
                      col=1)
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig = update_fig_style(fig)
    return fig
