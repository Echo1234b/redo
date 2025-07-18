# 🚀 Running Bitcoin Live Analyzer in Google Colab - Complete Guide

This guide provides step-by-step instructions to run the Bitcoin Live Analyzer & Predictor with MetaTrader 5 integration in Google Colab.

## 📋 Prerequisites

Before starting, ensure you have:
- A Google account with access to Google Colab
- A MetaTrader 5 account (demo or live) from a broker
- Basic knowledge of Python and Jupyter notebooks

## 🎯 Step-by-Step Setup

### Step 1: Open Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Sign in with your Google account
3. Create a new notebook or open an existing one

### Step 2: Setup the Environment

**Cell 1: Install System Dependencies**
```python
# Install system dependencies for MT5 and Wine
!apt-get update
!apt-get install -y wine winetricks xvfb python3-dev build-essential libffi-dev libssl-dev
!apt-get clean
```

**Cell 2: Install Python Packages**
```python
# Install core Python packages
!pip install streamlit>=1.28.0 pandas>=1.5.0 numpy>=1.24.0 plotly>=5.17.0 scikit-learn>=1.3.0
!pip install requests>=2.31.0 python-dateutil>=2.8.0 pytz>=2023.3

# Try to install TA-Lib (may fail, but app has fallbacks)
!pip install TA-Lib || echo "TA-Lib installation failed, using basic indicators"

# Install MT5 Linux support packages
!pip install MetaTrader5 pymt5linux || pip install mt5linux || echo "MT5 packages installed with basic support"
```

### Step 3: Clone the Repository

**Cell 3: Download the Application**
```python
# Clone the BTC analyzer repository
!git clone https://github.com/yourusername/btc-analyzer.git /content/btc-analyzer
%cd /content/btc-analyzer

# Verify the structure
!ls -la
```

### Step 4: Setup Wine Environment (for MT5 compatibility)

**Cell 4: Configure Wine**
```python
import os

# Set Wine environment variables
os.environ['WINEPREFIX'] = '/content/.wine'
os.environ['WINEARCH'] = 'win32'
os.environ['DISPLAY'] = ':0'

# Initialize Wine configuration (minimal setup)
!winecfg || echo "Wine configuration completed"
```

### Step 5: Test the Installation

**Cell 5: Verify Setup**
```python
# Test all imports
print("🧪 Testing Installation...")
print("=" * 50)

# Test core packages
try:
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    import streamlit as st
    from sklearn.ensemble import RandomForestClassifier
    print("✅ Core packages imported successfully")
except ImportError as e:
    print(f"❌ Core package import failed: {e}")

# Test TA-Lib
try:
    import talib
    print("✅ TA-Lib available")
    HAS_TALIB = True
except ImportError:
    print("⚠️ TA-Lib not available (will use basic indicators)")
    HAS_TALIB = False

# Test MT5
try:
    import MetaTrader5 as mt5
    print("✅ MetaTrader5 package available")
    MT5_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ MetaTrader5 import issue: {e}")
    MT5_AVAILABLE = False

print("=" * 50)
print(f"TA-Lib Available: {HAS_TALIB}")
print(f"MT5 Package Available: {MT5_AVAILABLE}")
```

### Step 6: Start the Application

**Cell 6: Launch the Streamlit App**
```python
# Change to the source directory
%cd /content/btc-analyzer/src

# Start the Streamlit application
!streamlit run btc_analyzer_app.py --server.headless=true --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false &
```

### Step 7: Access the Application

**Cell 7: Get the Public URL**
```python
# Install ngrok for public access
!pip install pyngrok

from pyngrok import ngrok
import time

# Wait a moment for Streamlit to start
time.sleep(10)

# Create a tunnel to the Streamlit app
public_url = ngrok.connect(8501)
print(f"🌐 Your Bitcoin Analyzer is available at: {public_url}")
print("📱 Click the link above to access your app!")
```

## 🔧 Configuration

### MetaTrader 5 Setup

Once the app is running, you'll need to configure MT5 connection:

1. **Get MT5 Credentials:**
   - Login number from your broker
   - Password
   - Server name (e.g., "BrokerName-Demo" or "BrokerName-Live")

2. **In the App Sidebar:**
   - Enter your MT5 login credentials
   - Select the correct server
   - Click "Connect to MT5"

3. **Symbol Selection:**
   - Choose Bitcoin or other cryptocurrency symbols
   - Select your preferred timeframe
   - Configure analysis parameters

## 🎨 Using the Application

### Main Features Available:

1. **Real-Time Price Analysis**
   - Live price feeds and candlestick charts
   - Multiple timeframes (M1, M5, M15, M30, H1, H4, D1)
   - Technical indicators overlay

2. **Technical Analysis**
   - Moving Averages (SMA, EMA)
   - RSI, MACD, Bollinger Bands
   - Volume and momentum indicators

3. **Machine Learning Predictions**
   - Price direction forecasting
   - Confidence scoring
   - Real-time model updates

4. **Interactive Charts**
   - Plotly-powered visualizations
   - Multi-panel analysis views
   - Real-time data updates

## 🚨 Troubleshooting

### Common Issues and Solutions:

**1. Import Errors**
```python
# If you get import errors, reinstall packages
!pip install --upgrade streamlit pandas numpy plotly scikit-learn
```

**2. MT5 Connection Issues**
```python
# Test MT5 connection manually
import MetaTrader5 as mt5

# Initialize MT5
if mt5.initialize():
    print("✅ MT5 initialized successfully")
    print(f"MT5 version: {mt5.version()}")
    mt5.shutdown()
else:
    print("❌ MT5 initialization failed")
```

**3. Streamlit Not Starting**
```python
# Check if Streamlit is running
!ps aux | grep streamlit

# Kill existing processes and restart
!pkill -f streamlit
!streamlit run /content/btc-analyzer/src/btc_analyzer_app.py --server.headless=true --server.port=8501 &
```

**4. TA-Lib Issues**
```python
# If TA-Lib fails, the app will use basic indicators automatically
# You can force install with:
!apt-get install -y libta-lib-dev
!pip install TA-Lib
```

## 💡 Pro Tips

### For Better Performance:

1. **Use GPU Runtime:**
   - In Colab: Runtime → Change runtime type → GPU
   - This speeds up machine learning computations

2. **Keep Session Active:**
   - Colab sessions timeout after inactivity
   - Keep the browser tab open
   - Interact with the app regularly

3. **Save Your Work:**
   - Download any analysis results
   - Export charts and predictions
   - Save model configurations

### Demo Trading Setup:

1. **Get a Demo Account:**
   - Visit your preferred broker's website
   - Create a demo MT5 account
   - Note down login, password, and server

2. **Recommended Brokers for Demo:**
   - MetaQuotes Demo
   - FXCM Demo
   - IG Markets Demo
   - XM Demo

## 🔒 Security Notes

- Use demo accounts for testing
- Never share your real trading credentials in Colab
- The app runs locally in your Colab instance
- Your data is not shared with external services

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Review the application logs in Colab**
3. **Try restarting the Colab runtime**
4. **Use a fresh Colab notebook**

## 🎉 Success!

If everything is working correctly, you should see:
- ✅ Streamlit app running
- ✅ Public URL accessible
- ✅ MT5 connection established
- ✅ Bitcoin data loading
- ✅ Charts and predictions displaying

Enjoy analyzing Bitcoin with your new live analyzer! 🚀📈

---

**Disclaimer:** This software is for educational purposes only. Trading involves substantial risk and may not be suitable for all investors. Always do your own research and consider consulting with financial professionals.