import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Load the previously saved stock data (ensure your CSV file has a "Date" column)
df = pd.read_csv("data.csv", parse_dates=["Date"])
df.set_index("Date", inplace=True)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stock Data Viewer"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Previously Fetched Stock Data", className="text-center text-primary mb-4"),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id="stock-graph",
                figure={
                    'data': [
                        go.Scatter(
                            x=df.index,
                            y=df['Close'],
                            mode='lines+markers',
                            name="Close Price"
                        )
                    ],
                    'layout': go.Layout(
                        title="Stock Price Over Time",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        hovermode='x unified',
                        template="plotly_white"
                    )
                }
            ),
            width=12
        )
    ])
], fluid=True, style={"padding": "30px"})

if __name__ == '__main__':
    app.run(debug=True)
