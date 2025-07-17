# 🚀 MetaTrader 5 Integration Guide for Bitcoin Live Analyzer

## 📋 **Overview**
This guide shows you how to integrate your Bitcoin Live Analyzer with MetaTrader 5 platform to import real-time and historical trading data directly from your MT5 terminal.

---

## 🔧 **Prerequisites**

### **1. MetaTrader 5 Terminal**
- **Download and install** MetaTrader 5 from [MetaQuotes website](https://www.metatrader5.com/)
- **Create a trading account** (demo or live) with a broker that supports MT5
- **Enable algorithmic trading** in MT5 settings

### **2. Python Environment**
- **Python 3.7+** installed
- **Google Colab** or local Python environment
- **Internet connection** for data synchronization

### **3. Trading Account**
- **MT5 Login credentials** (login, password, server)
- **Account with Bitcoin/Crypto symbols** (BTCUSD, ETHUSD, etc.)

---

## 📁 **Files Required**

### **🔥 Essential Files:**
1. **`metatrader_integration.py`** - Core MT5 integration module
2. **`btc_live_analyzer_mt5.py`** - Main app with MT5 support
3. **`colab_setup_mt5.py`** - Setup script with MT5 packages
4. **`requirements.txt`** - Dependencies list

### **📚 Optional Files:**
- **`test_app.py`** - Testing and diagnostics
- **`run_tunnel_mt5.py`** - Generated tunnel script

---

## 🛠️ **Installation Steps**

### **Step 1: Install MetaTrader 5 Terminal**
1. **Download MT5** from your broker or MetaQuotes
2. **Install and login** to your trading account
3. **Enable algorithmic trading**:
   - Go to `Tools` → `Options` → `Expert Advisors`
   - Check "Allow algorithmic trading"
   - Check "Allow DLL imports"

### **Step 2: Setup Python Environment**
```python
# In Google Colab or your Python environment
exec(open('colab_setup_mt5.py').read())
```

**This will install:**
- MetaTrader5 Python package
- All required dependencies
- Streamlit configuration
- Create run scripts

### **Step 3: Upload Files to Colab**
Upload these files to your Google Colab environment:
- `metatrader_integration.py`
- `btc_live_analyzer_mt5.py`
- `colab_setup_mt5.py`
- `requirements.txt`

---

## 🚀 **How to Use**

### **Step 1: Start the Application**
```python
# Run the MT5 version
exec(open('run_tunnel_mt5.py').read())
```

### **Step 2: Connect to MetaTrader 5**
1. **Open the app** using the ngrok URL
2. **Enter your MT5 credentials** in the sidebar:
   - **Login**: Your MT5 account number
   - **Password**: Your MT5 password
   - **Server**: Your broker's server name
3. **Click "Connect"**

### **Step 3: Select Trading Symbol**
1. **Search for symbols** (e.g., "BTC", "EUR", "USD")
2. **Select your desired symbol** from the dropdown
3. **Choose timeframe** (M1, M5, H1, H4, D1, etc.)

### **Step 4: Load and Analyze Data**
1. **Click "Load Data"** to import historical data
2. **View real-time prices** and technical indicators
3. **Get AI predictions** based on your data
4. **Monitor positions** and pending orders

---

## 📊 **Features Available**

### **🔥 Core Features:**
- **Real-time price data** from MT5
- **Historical OHLCV data** with multiple timeframes
- **Technical indicators** (RSI, MACD, Bollinger Bands, etc.)
- **Machine learning predictions** using your MT5 data
- **Account information** display
- **Position and order monitoring**

### **📈 Data Sources:**
- **Direct MT5 connection** (no external APIs needed)
- **Your broker's data feed** (real-time and accurate)
- **Multiple timeframes** (1min to 1month)
- **Any symbol** available in your MT5 account

### **🤖 AI Features:**
- **Price direction prediction** using ML models
- **Technical analysis** with professional indicators
- **Pattern recognition** (with TA-Lib)
- **Risk assessment** based on your account data

---

## 🎯 **Supported Symbols**

### **Crypto Pairs:**
- BTCUSD, ETHUSD, LTCUSD
- ADAUSD, DOTUSD, LINKUSD
- And any crypto pairs your broker offers

### **Forex Pairs:**
- EURUSD, GBPUSD, USDJPY
- AUDUSD, USDCAD, NZDUSD
- And all major/minor currency pairs

### **Other Instruments:**
- **Stocks**, **Indices**, **Commodities**
- **CFDs** and **Futures**
- Any symbol available in your MT5 terminal

---

## 🔧 **Configuration Options**

### **Connection Settings:**
- **Login**: Your MT5 account number
- **Password**: Your MT5 password  
- **Server**: Your broker's server (e.g., "Broker-Demo", "Broker-Live")

### **Data Settings:**
- **Symbol**: Trading instrument to analyze
- **Timeframe**: Chart period (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
- **Data Points**: Number of historical bars (100-5000)

### **Analysis Settings:**
- **Indicators**: Choose which technical indicators to display
- **ML Model**: Configure machine learning predictions
- **Chart Style**: Customize chart appearance

---

## ⚠️ **Troubleshooting**

### **Connection Issues:**
```python
# If MT5 connection fails:
1. Check if MetaTrader 5 terminal is running
2. Verify login credentials are correct
3. Ensure algorithmic trading is enabled
4. Try restarting MT5 terminal
```

### **Data Issues:**
```python
# If no data is loaded:
1. Check if the symbol exists in your MT5
2. Verify you have access to historical data
3. Try a different timeframe
4. Check your internet connection
```

### **Package Issues:**
```python
# If MetaTrader5 package fails to install:
pip install --upgrade MetaTrader5
pip install --upgrade pandas numpy
```

---

## 🔒 **Security Considerations**

### **Account Safety:**
- **Use demo accounts** for testing
- **Never share** your login credentials
- **Use read-only** analysis (no trading functions)
- **Monitor** your account activity

### **Data Privacy:**
- **Data stays local** to your MT5 terminal
- **No external API calls** for price data
- **Your broker's security** applies
- **Encrypted connections** to MT5

---

## 📋 **Complete Workflow**

### **Setup (One-time):**
```python
# 1. Install MT5 terminal and create account
# 2. Upload files to Colab
# 3. Run setup
exec(open('colab_setup_mt5.py').read())
```

### **Daily Usage:**
```python
# 1. Start the app
exec(open('run_tunnel_mt5.py').read())

# 2. Connect to MT5 (enter credentials)
# 3. Select symbol and timeframe
# 4. Load data and analyze
# 5. Get AI predictions and insights
```

---

## 🎯 **Advantages of MT5 Integration**

### **✅ Benefits:**
- **Real-time data** from your broker
- **No API limits** or rate restrictions
- **Accurate pricing** (your actual trading prices)
- **Complete symbol coverage** (all instruments you can trade)
- **Account integration** (see your positions and orders)
- **Professional data feed** (institutional quality)

### **🔥 Use Cases:**
- **Live trading analysis** with real broker data
- **Backtesting** with historical data
- **Multi-timeframe analysis** for better decisions
- **Risk management** with account monitoring
- **Automated insights** with AI predictions

---

## 📞 **Support**

### **Common Issues:**
1. **"Failed to initialize MT5"** - Check if MT5 terminal is running
2. **"Login failed"** - Verify credentials and server name
3. **"No symbols found"** - Check symbol availability in MT5
4. **"No data available"** - Try different timeframe or symbol

### **Resources:**
- **MetaTrader 5 Documentation**: [MQL5.com](https://www.mql5.com/en/docs)
- **Python MT5 Package**: [MetaTrader5 PyPI](https://pypi.org/project/MetaTrader5/)
- **Broker Support**: Contact your MT5 broker for account issues

---

## 🎉 **Ready to Trade with AI!**

Your Bitcoin Live Analyzer is now integrated with MetaTrader 5, giving you:
- **Professional trading data**
- **Real-time market analysis**
- **AI-powered predictions**
- **Complete account monitoring**

**Start analyzing your markets with institutional-grade data and AI insights!** 🚀📈