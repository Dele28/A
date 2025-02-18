from flask import Flask, render_template
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# List of 50 selected stocks
stocks = ['AAPL', 'MSFT', 'TSLA', 'AMD', 'NVDA', 'PLUG', 'F', 'GE', 'T', 'XOM',
          'BAC', 'NIO', 'CCL', 'UAL', 'RIVN', 'SOFI', 'DNA', 'INTC', 'SNAP', 'WFC',
          'PFE', 'C', 'KOS', 'GPRO', 'AAL', 'LYFT', 'UBER', 'DIS', 'VZ', 'GM',
          'BABA', 'XPEV', 'COIN', 'RBLX', 'NKLA', 'MARA', 'RIOT', 'GME', 'AMC', 'CVNA',
          'AFRM', 'DKNG', 'FUBO', 'LCID', 'HYLN', 'OPEN', 'QS', 'SPCE', 'WKHS', 'ZNGA']

# Function to calculate buy/sell signals
def get_signal(data):
    short_window = 14
    long_window = 50
    data['SMA_14'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_50'] = data['Close'].rolling(window=long_window).mean()
    
    buy_signal = data['SMA_14'].iloc[-1] > data['SMA_50'].iloc[-1] and data['SMA_14'].iloc[-2] <= data['SMA_50'].iloc[-2]
    sell_signal = data['SMA_14'].iloc[-1] < data['SMA_50'].iloc[-1] and data['SMA_14'].iloc[-2] >= data['SMA_50'].iloc[-2]
    
    return 'buy' if buy_signal else 'sell' if sell_signal else 'hold'

@app.route('/')
def index():
    stock_data = []
    
    for stock in stocks:
        try:
            data = yf.download(stock, period='3mo', interval='1d')
            if data.empty:
                continue
            
            signal = get_signal(data)
            last_close = data['Close'].iloc[-1]
            
            stock_data.append({'symbol': stock, 'price': round(last_close, 2), 'signal': signal})
        except Exception as e:
            print(f"Error fetching {stock}: {e}")
    
    # Move buy/sell signals to the top
    stock_data.sort(key=lambda x: (x['signal'] == 'buy', x['signal'] == 'sell'), reverse=True)
    
    return render_template('index.html', stocks=stock_data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    app.run(host='0.0.0.0', port=port, debug=False)  # Debug should be off in production
