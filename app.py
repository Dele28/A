from flask import Flask, render_template, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# List of tracked stocks
tracked_stocks = ["AAPL", "MSFT", "INTC", "GOOGL"]

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100
        
        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "change_percent": round(change_percent, 2)
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

@app.route('/')
def index():
    return render_template("index.html", stocks=[get_stock_data(ticker) for ticker in tracked_stocks])

@app.route('/api/stocks')
def api_stocks():
    return jsonify([get_stock_data(ticker) for ticker in tracked_stocks])

if __name__ == '__main__':
    app.run(debug=True)