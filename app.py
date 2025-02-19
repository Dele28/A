from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# List of tracked stocks (Initial List)
tracked_stocks = ["AAPL", "MSFT", "INTC", "GOOGL", "TSLA", "AMZN", "NVDA", "META"]

# Store buy/sell signals
signals = []

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        if len(hist) < 2:
            return {"ticker": ticker, "error": "Not enough data"}
        
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100

        # Determine buy/sell signals
        signal = None
        if change_percent > 5:
            signal = "Buy"
        elif change_percent < -5:
            signal = "Sell"

        stock_data = {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "change_percent": round(change_percent, 2),
            "signal": signal
        }
        
        if signal:
            signals.append(stock_data)
            signals.sort(key=lambda x: abs(x['change_percent']), reverse=True)

        return stock_data
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

@app.route('/')
def index():
    stock_data = [get_stock_data(ticker) for ticker in tracked_stocks]
    return render_template("index.html", stocks=stock_data, signals=signals)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    new_stock = request.json.get("ticker").upper()
    if new_stock and new_stock not in tracked_stocks:
        tracked_stocks.append(new_stock)
    return jsonify({"stocks": tracked_stocks})

@app.route('/remove_stock', methods=['POST'])
def remove_stock():
    stock_to_remove = request.json.get("ticker").upper()
    if stock_to_remove in tracked_stocks:
        tracked_stocks.remove(stock_to_remove)
    return jsonify({"stocks": tracked_stocks})

@app.route('/api/stocks')
def api_stocks():
    return jsonify([get_stock_data(ticker) for ticker in tracked_stocks])

if __name__ == '__main__':
    app.run(debug=True)
