from flask import Flask, render_template, jsonify
import yfinance as yf

app = Flask(__name__)

# Expanded list of tracked stocks
tracked_stocks = [
    "AAPL", "MSFT", "INTC", "GOOGL", "GM", "MGTI", "IGOT", "BRGO", "STIM", "APPS",
    "F", "INLF", "LINE", "KDLY", "JZXN", "MVST", "AIFF", "SSET", "AFFU", "MATH",
    "CBDL", "SLQT", "OPRT", "BMRA", "TPHS", "AXIL", "BSLK", "NOTE", "GPAK", "SPAI",
    "PBIO", "AGSS", "TIVC", "FORA", "MINM", "FEMY", "LIPO", "ZH", "SKBL", "PXHI", "AVR",
    "ETST", "CTSO", "LUCD", "ORGS", "RBBN", "UDMY", "EMMA", "PEV", "SRM", "NIXX", "SKVI",
    "NISN", "FRZT", "AHT", "BROG", "WAST", "APCX", "SKKY", "ALLO", "BNAI", "SNAX", "GRST",
    "FHTX", "ENTA", "PAVM", "DBGI", "LEEN", "SPGC", "QIND", "OMGA", "ZCAR", "CAUD", "WBBA",
    "MTEM", "CYN", "MOND"
]

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        if len(hist) < 2:
            return {"ticker": ticker, "error": "Not enough data"}
        
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100
        signal = "buy" if change_percent > 2 else "sell" if change_percent < -2 else "hold"
        
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
    stocks = sorted([get_stock_data(ticker) for ticker in tracked_stocks], key=lambda x: x.get("change_percent", 0), reverse=True)
    return render_template("index.html", stocks=stocks)

@app.route('/api/stocks')
def api_stocks():
    return jsonify([get_stock_data(ticker) for ticker in tracked_stocks])

if __name__ == '__main__':
    app.run(debug=True)
