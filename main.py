# === Imports ===
# Dash framework and components
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

# Plotting and data processing
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf

# System and time handling
from datetime import datetime, timedelta
import os
import time

# MongoDB integration
from pymongo import MongoClient
from pymongo.operations import UpdateOne
from pymongo.errors import BulkWriteError

# === MongoDB Init ===
client = MongoClient('mongodb://localhost:27017/')
db = client['stock_market']

# === Dash App Init ===
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]
)
app.title = "Stock Data Viewer and Storage"

# === Custom HTML Template Load ===
app._favicon = None
with open('c:\\rajkrish\\--\\templates\\index.html', 'r') as f:
    app.index_string = f.read()

# === Options ===
period_options = [
    {'label': '1 Day', 'value': '1d'},
    {'label': '5 Days', 'value': '5d'},
    {'label': '1 Month', 'value': '1mo'},
    {'label': '2 Months', 'value': '2mo'},
    {'label': '3 Months', 'value': '3mo'}
]

market_options = [
    {'label': 'US Market', 'value': 'US'},
    {'label': 'Indian Market (NSE)', 'value': 'NSE'}
]

# === Functions ===
def get_stock_symbol(base_symbol, market):
    return f"{base_symbol}.NS" if market == 'NSE' else base_symbol

def process_stock_file(filepath, symbol):
    try:
        collection_name = f'{symbol}_collection'
        stock_collection = db[collection_name]
        df = pd.read_csv(filepath)

        if df.empty:
            print(f"Warning: {symbol} data is empty, skipping...")
            return None

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], utc=True)

        bulk_operations = []
        for _, row in df.iterrows():
            stock_data = {
                'symbol': symbol,
                'data': row.to_dict(),
                'last_updated': datetime.now(),
                'source_file': filepath
            }
            bulk_operations.append(
                UpdateOne(
                    {'symbol': symbol, 'data.Date': stock_data['data']['Date']},
                    {'$set': stock_data},
                    upsert=True
                )
            )

        if bulk_operations:
            result = stock_collection.bulk_write(bulk_operations, ordered=False)
            print(f"MongoDB: Processed {symbol}: {result.modified_count} modified, {result.upserted_count} inserted")

        return df

    except Exception as e:
        print(f"Error processing {symbol} for MongoDB: {str(e)}")
        return None

def download_stock_data(symbol, period='1mo', market='US'):
    try:
        yahoo_symbol = get_stock_symbol(symbol, market)
        stock = yf.Ticker(yahoo_symbol)
        df = stock.history(period=period)

        if df.empty:
            print(f"No data found for {yahoo_symbol}")
            return None

        if market == 'NSE':
            df.index = df.index.tz_convert('Asia/Kolkata')

        output_path = f"c:\\rajkrish\\--\\stock_data\\{symbol}_stock_data.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path)

        df = process_stock_file(output_path, symbol)
        return df

    except Exception as e:
        print(f"Error downloading data for {symbol}: {str(e)}")
        return None

# === Callback ===
@app.callback(
    Output("stock-graph", "figure"),
    Input("fetch-button", "n_clicks"),
    State("stock-input", "value"),
    State("period-dropdown", "value"),
    State("market-dropdown", "value")
)
def update_graph(n_clicks, symbols_input, period, market):
    if not symbols_input:
        raise PreventUpdate

    try:
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        traces = []

        for symbol in symbols:
            df = download_stock_data(symbol, period, market)
            if df is not None:
                traces.append(go.Scatter(
                    x=df.index,
                    y=df['Close'],
                    mode='lines+markers',
                    name=f"{symbol} ({market})"
                ))

        title = "US Stock Prices" if market == 'US' else "Indian Stock Prices (NSE)"
        currency = "USD" if market == 'US' else "INR"

        return {
            'data': traces,
            'layout': go.Layout(
                title=f"{title} Over Time",
                xaxis_title="Date",
                yaxis_title=f"Price ({currency})",
                hovermode='x unified',
                template="plotly_white"
            )
        }

    except Exception as e:
        return {
            'data': [],
            'layout': go.Layout(title=f"Error: {str(e)}", template="plotly_white")
        }

# === Layout ===
app.layout = html.Div([
    html.Div([
        html.H1("Global Stock Data Viewer", className="text-center text-primary")
    ], className="header"),

    html.Div([
        html.Div([
            dbc.Input(
                id="stock-input",
                type="text",
                placeholder="US: AAPL,MSFT | India: RELIANCE,TCS,INFY",
                value="",
                className="mb-3"
            ),
            dcc.Dropdown(
                id="market-dropdown",
                options=market_options,
                value=None,
                placeholder="Select Market",
                className="mb-3"
            ),
            dcc.Dropdown(
                id="period-dropdown",
                options=period_options,
                value=None,
                placeholder="Select Time Period",
                className="mb-3"
            ),
            dbc.Button("Fetch Data", id="fetch-button", color="primary", className="w-100 mb-3"),
            html.Div("For Indian stocks, use NSE symbols (e.g., RELIANCE, TCS, INFY)",
                     className="text-muted small")
        ], className="input-panel"),

        html.Div([
            dcc.Graph(id="stock-graph", className="dash-graph", config={'displayModeBar': True})
        ], className="graph-panel")
    ], className="content-row")
], className="app-container")

if __name__ == '__main__':
    app.run(debug=True)
