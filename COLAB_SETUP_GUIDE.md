# Running MetaTrader5 from Google Colab - Complete Guide

## 🎯 Overview

This guide shows you how to run your MetaTrader5 Python applications from Google Colab. Since MT5 requires a Windows environment and Colab runs on Linux servers, we'll use several approaches depending on your needs.

## 🏗️ Architecture Options

### Option 1: Colab → Local MT5 (Recommended for Development)
```
Google Colab (Cloud) ←→ Internet ←→ Your Local Computer (MT5 + Bridge)
```

### Option 2: Colab → Cloud MT5 (Advanced)
```
Google Colab (Cloud) ←→ Cloud VPS (Windows + MT5)
```

### Option 3: Colab Data Analysis Only
```
Google Colab (Cloud) ← Data Files ← Local MT5 Export
```

## 🚀 Method 1: Colab with Local MT5 Connection

### Step 1: Prepare Your Local Environment

First, set up MT5 on your local machine:

#### For Windows Users:
```bash
# Install MetaTrader5
pip install MetaTrader5 pandas numpy matplotlib

# Test local connection
python test_app.py
```

#### For Linux Users:
```bash
# Use our automated setup
./setup_wine_mt5.sh

# Start MT5 and bridge
./start_mt5.sh
./start_mt5_bridge.sh
```

### Step 2: Set Up Tunneling (ngrok)

To connect Colab to your local MT5, we need to expose your local connection:

#### Install ngrok on your local machine:
```bash
# Download and install ngrok
wget https://bin.equinox.io/c/bVanNKlp6Z2/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Sign up at https://ngrok.com and get your auth token
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Step 3: Create MT5 Bridge Server (Local)

Create a simple HTTP bridge on your local machine:

```python
# Save as mt5_bridge_server.py on your local machine
from flask import Flask, jsonify, request
import MetaTrader5 as mt5
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)

# Initialize MT5 connection
if not mt5.initialize():
    print("Failed to initialize MT5")
    quit()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "mt5_connected": True})

@app.route('/account_info', methods=['GET'])
def get_account_info():
    try:
        account_info = mt5.account_info()
        if account_info is None:
            return jsonify({"error": "Failed to get account info"}), 500
        
        return jsonify({
            "login": account_info.login,
            "balance": account_info.balance,
            "equity": account_info.equity,
            "currency": account_info.currency,
            "leverage": account_info.leverage
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_rates', methods=['POST'])
def get_rates():
    try:
        data = request.json
        symbol = data.get('symbol', 'EURUSD')
        timeframe = getattr(mt5, f"TIMEFRAME_{data.get('timeframe', 'M1')}")
        count = data.get('count', 100)
        
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None:
            return jsonify({"error": "Failed to get rates"}), 500
        
        # Convert to DataFrame and then to JSON
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        return jsonify({
            "symbol": symbol,
            "timeframe": data.get('timeframe', 'M1'),
            "count": len(df),
            "data": df.to_dict('records')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_tick', methods=['POST'])
def get_tick():
    try:
        data = request.json
        symbol = data.get('symbol', 'EURUSD')
        
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return jsonify({"error": f"Failed to get tick for {symbol}"}), 500
        
        return jsonify({
            "symbol": symbol,
            "time": datetime.fromtimestamp(tick.time).isoformat(),
            "bid": tick.bid,
            "ask": tick.ask,
            "last": tick.last,
            "volume": tick.volume
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting MT5 Bridge Server...")
    print("Make sure MT5 terminal is running and logged in!")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 4: Start Local Bridge Server

On your local machine:

```bash
# Install Flask if not already installed
pip install flask

# Start the bridge server
python mt5_bridge_server.py

# In another terminal, expose it with ngrok
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

### Step 5: Google Colab Setup

Open a new Google Colab notebook and run these cells:

#### Cell 1: Install Dependencies
```python
# Install required packages
!pip install requests pandas numpy matplotlib seaborn plotly

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
```

#### Cell 2: MT5 Connection Class
```python
class MT5ColabConnector:
    def __init__(self, bridge_url):
        self.bridge_url = bridge_url.rstrip('/')
        self.session = requests.Session()
    
    def test_connection(self):
        """Test connection to MT5 bridge"""
        try:
            response = self.session.get(f"{self.bridge_url}/health", timeout=10)
            if response.status_code == 200:
                print("✅ Successfully connected to MT5 bridge!")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_account_info(self):
        """Get MT5 account information"""
        try:
            response = self.session.get(f"{self.bridge_url}/account_info", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Account: {data['login']}")
                print(f"💰 Balance: {data['balance']} {data['currency']}")
                print(f"💵 Equity: {data['equity']} {data['currency']}")
                print(f"📈 Leverage: 1:{data['leverage']}")
                return data
            else:
                print(f"❌ Failed to get account info: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting account info: {e}")
            return None
    
    def get_rates(self, symbol="EURUSD", timeframe="M1", count=100):
        """Get historical rates"""
        try:
            payload = {
                "symbol": symbol,
                "timeframe": timeframe,
                "count": count
            }
            response = self.session.post(
                f"{self.bridge_url}/get_rates", 
                json=payload, 
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['data'])
                df['time'] = pd.to_datetime(df['time'])
                df.set_index('time', inplace=True)
                print(f"📈 Retrieved {len(df)} {timeframe} bars for {symbol}")
                return df
            else:
                print(f"❌ Failed to get rates: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting rates: {e}")
            return None
    
    def get_current_price(self, symbol="EURUSD"):
        """Get current price"""
        try:
            payload = {"symbol": symbol}
            response = self.session.post(
                f"{self.bridge_url}/get_tick", 
                json=payload, 
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print(f"💱 {symbol} - Bid: {data['bid']}, Ask: {data['ask']}")
                return data
            else:
                print(f"❌ Failed to get price: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting price: {e}")
            return None

# Replace with your ngrok URL
BRIDGE_URL = "https://your-ngrok-url.ngrok.io"  # ⚠️ UPDATE THIS!

# Create connector
mt5 = MT5ColabConnector(BRIDGE_URL)
```

#### Cell 3: Test Connection
```python
# Test the connection
if mt5.test_connection():
    print("🎉 Ready to trade!")
    
    # Get account info
    account = mt5.get_account_info()
    
    # Get current price
    price = mt5.get_current_price("EURUSD")
else:
    print("❌ Connection failed. Check:")
    print("1. MT5 terminal is running and logged in")
    print("2. Bridge server is running (python mt5_bridge_server.py)")
    print("3. ngrok is running (ngrok http 5000)")
    print("4. BRIDGE_URL is correct")
```

#### Cell 4: Get and Analyze Data
```python
# Get historical data
symbol = "EURUSD"
timeframe = "H1"  # Options: M1, M5, M15, M30, H1, H4, D1
count = 200

df = mt5.get_rates(symbol, timeframe, count)

if df is not None:
    print(f"\n📊 Data Summary for {symbol}:")
    print(f"Period: {df.index.min()} to {df.index.max()}")
    print(f"Latest Price: {df['close'].iloc[-1]:.5f}")
    print(f"24h Change: {((df['close'].iloc[-1] / df['close'].iloc[-24]) - 1) * 100:.2f}%")
    print(f"High/Low: {df['high'].max():.5f} / {df['low'].min():.5f}")
    
    # Display last few rows
    print(f"\nLatest {timeframe} data:")
    print(df[['open', 'high', 'low', 'close', 'tick_volume']].tail())
```

#### Cell 5: Create Interactive Charts
```python
# Create interactive candlestick chart
if df is not None:
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'{symbol} Price Chart', 'Volume'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name=symbol
        ),
        row=1, col=1
    )

    # Volume chart
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['tick_volume'],
            name='Volume',
            marker_color='rgba(158,202,225,0.6)'
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        title=f'{symbol} Analysis - {timeframe} Timeframe',
        xaxis_rangeslider_visible=False,
        height=600,
        showlegend=False
    )

    fig.show()
```

#### Cell 6: Technical Analysis
```python
# Add technical indicators
def add_technical_indicators(df):
    """Add common technical indicators"""
    
    # Simple Moving Averages
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_Middle'] = df['close'].rolling(window=20).mean()
    bb_std = df['close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
    
    return df

if df is not None:
    df = add_technical_indicators(df)
    
    # Display analysis
    print(f"📊 Technical Analysis for {symbol}:")
    print(f"Current Price: {df['close'].iloc[-1]:.5f}")
    print(f"SMA 20: {df['SMA_20'].iloc[-1]:.5f}")
    print(f"SMA 50: {df['SMA_50'].iloc[-1]:.5f}")
    print(f"RSI: {df['RSI'].iloc[-1]:.2f}")
    print(f"Bollinger Bands: {df['BB_Lower'].iloc[-1]:.5f} - {df['BB_Upper'].iloc[-1]:.5f}")
    
    # Trading signals
    current_price = df['close'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    
    print(f"\n🎯 Simple Trading Signals:")
    if current_price > df['SMA_20'].iloc[-1] and rsi < 70:
        print("📈 Potential BUY signal (Price above SMA20, RSI not overbought)")
    elif current_price < df['SMA_20'].iloc[-1] and rsi > 30:
        print("📉 Potential SELL signal (Price below SMA20, RSI not oversold)")
    else:
        print("⏸️ No clear signal - Wait for better opportunity")
```

## 🚀 Method 2: Cloud VPS Setup (Advanced)

For a more permanent solution, you can set up a Windows VPS in the cloud:

### Step 1: Create Windows VPS
1. Use services like AWS EC2, Google Cloud, or DigitalOcean
2. Create a Windows Server instance
3. Install MetaTrader5 and Python

### Step 2: Set Up Remote Access
```python
# In Colab, connect to your cloud VPS
import paramiko

def connect_to_vps(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    return ssh

# Connect and run MT5 commands
ssh = connect_to_vps("your-vps-ip", "username", "password")
stdin, stdout, stderr = ssh.exec_command("python your_mt5_script.py")
```

## 🚀 Method 3: Data Analysis Only

If you only need data analysis (not live trading), export data locally and upload to Colab:

### Step 1: Export Data Locally
```python
# Run this on your local machine with MT5
import MetaTrader5 as mt5
import pandas as pd

mt5.initialize()

# Export historical data
symbols = ["EURUSD", "GBPUSD", "USDJPY"]
timeframes = [mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1]

for symbol in symbols:
    for tf in timeframes:
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, 1000)
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        tf_name = {mt5.TIMEFRAME_H1: "H1", mt5.TIMEFRAME_H4: "H4", mt5.TIMEFRAME_D1: "D1"}[tf]
        filename = f"{symbol}_{tf_name}_data.csv"
        df.to_csv(filename, index=False)
        print(f"Exported {filename}")

mt5.shutdown()
```

### Step 2: Upload to Colab
```python
# In Colab
from google.colab import files
import pandas as pd

# Upload CSV files
uploaded = files.upload()

# Load and analyze data
for filename in uploaded.keys():
    df = pd.read_csv(filename)
    df['time'] = pd.to_datetime(df['time'])
    print(f"Loaded {filename}: {len(df)} rows")
    
    # Your analysis here
    print(df.tail())
```

## 🔧 Troubleshooting

### Common Issues:

1. **Connection Timeout**:
   ```python
   # Increase timeout in requests
   response = requests.get(url, timeout=30)
   ```

2. **ngrok URL Changes**:
   ```python
   # Check current ngrok URL
   import requests
   tunnels = requests.get("http://localhost:4040/api/tunnels").json()
   public_url = tunnels['tunnels'][0]['public_url']
   print(f"Current ngrok URL: {public_url}")
   ```

3. **MT5 Connection Lost**:
   ```python
   # Add connection retry logic
   def retry_connection(func, max_retries=3):
       for attempt in range(max_retries):
           try:
               return func()
           except Exception as e:
               if attempt == max_retries - 1:
                   raise e
               print(f"Retry {attempt + 1}/{max_retries}")
               time.sleep(5)
   ```

## 🚨 Security Notes

- Never commit real account credentials to Colab notebooks
- Use demo accounts for testing
- Be careful with public ngrok URLs
- Consider VPN for additional security
- Monitor your MT5 account for unexpected activity

## 🎯 Best Practices

1. **Start with Demo Account**: Always test with demo accounts first
2. **Use Environment Variables**: Store sensitive data securely
3. **Implement Error Handling**: Add try-catch blocks for robust code
4. **Monitor Performance**: Watch for latency and connection issues
5. **Regular Backups**: Save important analysis and strategies

Your MetaTrader5 application is now ready to run from Google Colab! 🚀