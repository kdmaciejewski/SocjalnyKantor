from dash import Dash, dcc, html
import plotly.express as px
from base64 import b64encode
import io
from datetime import datetime
import yfinance as yf

if __name__ == '__main__':

    app = Dash(__name__)

    buffer = io.StringIO()

    cryptocurrencies = ['BTC-USD', 'ETH-USD', 'DOGE-USD', 'BNB-USD']

    df = yf.download(cryptocurrencies, start='2020-01-01',
                     end=datetime.today().strftime('%Y-%m-%d'))
    df.isnull().any()
    adj_close = df['Adj Close']
    fig = px.line(adj_close, y="BTC-USD")

    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()

    app.layout = html.Div([
        html.P("Wykres BTC-USD", style={"font-family": "Arial", "font-size": "26px"}),
        dcc.Graph(id="graph", figure=fig),
        html.A(
            html.Button("Download as HTML"),
            id="download",
            href="data:text/html;base64," + encoded,
            download="graph_btc.html"
        )
    ])

    app.run_server(debug=True)