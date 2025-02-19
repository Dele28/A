from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# List of tracked stocks (initial default ones)
tracked_stocks = ["AAPL", "MSFT", "INTC", "GOOGL"]

# Store buy/sell signals
signals = []

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100

        # Determine buy/sell signals
        signal = ""
        if change_percent > 2:
            signal = "BUY"
        elif change_percent < -2:
            signal = "SELL"

        if signal:
            signals.append({"ticker": ticker, "signal": signal, "price": current_price})
            signals.sort(key=lambda x: x['price'], reverse=True)  # Most recent signals on top

        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "change_percent": round(change_percent, 2),
            "signal": signal
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

@app.route('/')
def index():
    stocks = [get_stock_data(ticker) for ticker in tracked_stocks]
    return render_template("index.html", stocks=stocks, signals=signals)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    new_ticker = request.form.get("ticker").upper()
    if new_ticker and new_ticker not in tracked_stocks:
        tracked_stocks.append(new_ticker)
    return jsonify({"stocks": tracked_stocks})

@app.route('/api/stocks')
def api_stocks():
    return jsonify([get_stock_data(ticker) for ticker in tracked_stocks])

if __name__ == '__main__':
    app.run(debug=True)
