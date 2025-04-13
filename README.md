# 📈 Stock Data Viewer Dashboard

A responsive web dashboard built using **Dash (Plotly)** that allows users to:
- View historical stock data from **Yahoo Finance**
- Support for both **US** and **Indian (NSE)** markets
- Download and store stock data into **MongoDB**
- Display interactive time-series graphs

---

## 🚀 Features

✅ Fetch live stock data using [yfinance](https://github.com/ranaroussi/yfinance)  
✅ Supports multiple stocks input (comma-separated)  
✅ Choose from US or NSE markets  
✅ Select data periods: 1d, 5d, 1mo, 2mo, 3mo  
✅ Data saved to **MongoDB** with update and deduplication  
✅ Interactive Plotly graph (zoom, pan, export)  
✅ Modern UI using Bootstrap & custom HTML template

---

## 📦 Tech Stack

| Tech        | Description                                  |
|-------------|----------------------------------------------|
| Python      | Core backend language                        |
| Dash        | Frontend framework for data visualization    |
| yfinance    | Stock market data fetching                   |
| Plotly      | Charting library used by Dash                |
| MongoDB     | NoSQL database to store and update stock data|
| Pandas      | Data manipulation and CSV export             |
| Bootstrap   | Clean and responsive UI layout               |

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/rajkrish63/stock-analysis-.git
cd stock-data-viewer
