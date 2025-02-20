import os
import sqlite3
import time
import yfinance as yf
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_FILE = "stocks.db"

# Initialize Database
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stocks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ticker TEXT UNIQUE NOT NULL,
                        current_price REAL,
                        change_percent REAL,
                        signal TEXT,
                        timestamp INTEGER
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS tracked_stocks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ticker TEXT UNIQUE NOT NULL
                    )''')
        conn.commit()

# Fetch stock data from Yahoo Finance
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        if len(hist) < 2:
            return (ticker, None, None, "NO DATA", int(time.time()))
        
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100
        
        signal = "BUY" if change_percent > 2 else "SELL" if change_percent < -2 else "HOLD"
        return (ticker, round(current_price, 2), round(change_percent, 2), signal, int(time.time()))
    except:
        return (ticker, None, None, "ERROR", int(time.time()))

# Update stock data in the database
def update_stock_data():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT ticker FROM tracked_stocks")
        tracked_stocks = [row[0] for row in c.fetchall()]
        
        for ticker in tracked_stocks:
            data = get_stock_data(ticker)
            c.execute('''INSERT INTO stocks (ticker, current_price, change_percent, signal, timestamp)
                         VALUES (?, ?, ?, ?, ?) ON CONFLICT(ticker) DO UPDATE SET
                         current_price=excluded.current_price,
                         change_percent=excluded.change_percent,
                         signal=excluded.signal,
                         timestamp=excluded.timestamp''', data)
        conn.commit()

@app.route('/')
def index():
    print("Serving index.html")  # Debugging log
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT ticker, current_price, change_percent, signal FROM stocks ORDER BY timestamp DESC")
        stocks = [dict(zip(["ticker", "current_price", "change_percent", "signal"], row)) for row in c.fetchall()]
    return render_template("index.html", stocks=stocks)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    ticker = request.json.get("ticker", "").upper()
    if not ticker:
        return jsonify({"error": "No ticker provided"}), 400
    
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO tracked_stocks (ticker) VALUES (?)", (ticker,))
        conn.commit()
    return jsonify({"message": "Stock added"})

@app.route('/remove_stock', methods=['POST'])
def remove_stock():
    ticker = request.json.get("ticker", "").upper()
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM tracked_stocks WHERE ticker = ?", (ticker,))
        c.execute("DELETE FROM stocks WHERE ticker = ?", (ticker,))
        conn.commit()
    return jsonify({"message": "Stock removed"})

if __name__ == '__main__':
    init_db()
    update_stock_data()
    app.run(debug=True)
