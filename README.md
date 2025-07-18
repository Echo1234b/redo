# ₿ Bitcoin Live Analyzer & Predictor - MT5 Edition

A powerful, real-time Bitcoin and cryptocurrency analyzer with MetaTrader 5 integration, featuring advanced technical analysis, machine learning predictions, and live data streaming.

![Bitcoin Analyzer](https://img.shields.io/badge/Bitcoin-Analyzer-orange.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![MetaTrader5](https://img.shields.io/badge/MetaTrader5-Integrated-green.svg)

## 🚀 Features

### 📊 Real-Time Data Analysis
- Live price feeds from MetaTrader 5
- Support for Bitcoin and multiple cryptocurrencies
- Multiple timeframes (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
- Real-time account monitoring

### 📈 Advanced Technical Analysis
- **Moving Averages**: SMA, EMA with multiple periods
- **Momentum Indicators**: RSI, MACD, Stochastic
- **Volatility Indicators**: Bollinger Bands, ATR
- **Trend Indicators**: ADX, CCI, Williams %R
- **Volume Analysis**: MFI and volume-based indicators

### 🤖 Machine Learning Predictions
- Random Forest price direction prediction
- Feature engineering with technical indicators
- Confidence scoring for predictions
- Real-time model training and updates

### 🎨 Interactive Visualizations
- Professional candlestick charts with Plotly
- Multi-panel technical analysis views
- Real-time price updates
- Customizable chart layouts

### 🌐 Cross-Platform Support
- **Windows**: Native MetaTrader 5 support
- **Linux**: Wine-based MT5 bridge
- **Google Colab**: Complete setup automation

## 📋 Prerequisites

- Python 3.8 or higher
- MetaTrader 5 account (demo or live)
- Internet connection for data feeds

## 🛠️ Installation

### Option 1: Windows Quick Setup (Recommended)

1. **Download the app** and extract to a folder
2. **Run automated setup**: Double-click `windows_setup.bat`
3. **Start the app**: Run `python run_app.py`
4. **Open browser**: Go to http://localhost:8501

📖 **Detailed Windows Guide**: [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)

### Option 2: Manual Installation (All Platforms)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/btc-analyzer.git
cd btc-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python run_app.py
# OR
streamlit run src/btc_analyzer_app.py
```

### Option 2: Google Colab Setup

1. **Run the setup script in Colab**
```python
!wget https://raw.githubusercontent.com/yourusername/btc-analyzer/main/scripts/colab_setup.py
!python colab_setup.py
```

2. **Clone and start the application**
```python
!git clone https://github.com/yourusername/btc-analyzer.git /content/btc-analyzer
!python /content/start_btc_analyzer.py
```

### Option 3: Linux with Wine (Manual Setup)

1. **Install Wine and dependencies**
```bash
sudo apt update
sudo apt install wine winetricks xvfb
```

2. **Setup Python environment**
```bash
pip install -r requirements.txt
pip install pymt5linux  # or mt5linux
```

3. **Configure Wine for MT5**
```bash
winecfg  # Set to Windows 10
```

## 🔧 Configuration

### MetaTrader 5 Setup

1. **Download and install MT5**
   - Windows: Download from MetaQuotes website
   - Linux: Use Wine to install Windows version

2. **Enable algorithmic trading**
   - In MT5: Tools → Options → Expert Advisors
   - Check "Allow automated trading"
   - Check "Allow DLL imports"

3. **Get broker credentials**
   - Login number
   - Password
   - Server name

### Application Configuration

The application uses the sidebar for all configuration:

1. **MT5 Connection**
   - Enter your login credentials
   - Select broker server
   - Click "Connect to MT5"

2. **Symbol Selection**
   - Choose from available symbols
   - Bitcoin symbols are prioritized
   - View symbol information

3. **Analysis Parameters**
   - Select timeframe
   - Adjust data points
   - Configure indicators

## 📱 Usage

### Getting Started

1. **Launch the application**
```bash
streamlit run src/btc_analyzer_app.py
```

2. **Connect to MetaTrader 5**
   - Use the sidebar connection form
   - Enter your MT5 credentials
   - Verify connection status

3. **Select trading symbol**
   - Choose BTCUSD or other crypto pairs
   - Review symbol information
   - Select preferred timeframe

4. **Load and analyze data**
   - Click "Load Data" to fetch historical data
   - View technical indicators
   - Check AI predictions

### Key Features Explained

#### 🎯 Price Prediction
- Uses Random Forest machine learning
- Predicts next period price direction
- Provides confidence levels
- Updates in real-time

#### 📊 Technical Indicators
- **RSI**: Relative Strength Index (14-period)
- **MACD**: Moving Average Convergence Divergence
- **Bollinger Bands**: 20-period with 2 standard deviations
- **Volume Analysis**: 20-period volume moving average

#### 📈 Chart Analysis
- **Candlestick Charts**: OHLC price data
- **Volume Bars**: Trading volume analysis
- **Indicator Overlays**: Technical analysis overlays
- **Multi-timeframe**: Switch between different periods

## 🏗️ Project Structure

```
btc-analyzer/
├── src/
│   ├── btc_analyzer_app.py      # Main Streamlit application
│   └── mt5_integration.py       # MetaTrader 5 integration module
├── scripts/
│   └── colab_setup.py          # Google Colab setup automation
├── docs/
│   ├── installation.md         # Detailed installation guide
│   └── troubleshooting.md      # Common issues and solutions
├── config/
│   └── settings.py             # Application configuration
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🔍 Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **MetaTrader5**: MT5 API integration
- **Pandas/NumPy**: Data processing
- **Plotly**: Interactive charts
- **Scikit-learn**: Machine learning
- **TA-Lib**: Technical analysis (optional)

### Data Flow

1. **Connection**: App connects to MT5 terminal
2. **Data Retrieval**: Historical and real-time data fetched
3. **Processing**: Technical indicators calculated
4. **Analysis**: ML model training and prediction
5. **Visualization**: Interactive charts and metrics
6. **Updates**: Real-time data refresh

### Supported Symbols

- **Cryptocurrencies**: BTCUSD, ETHUSD, LTCUSD, etc.
- **Forex Pairs**: EURUSD, GBPUSD, USDJPY, etc.
- **Indices**: US30, SPX500, NAS100, etc.
- **Commodities**: XAUUSD, XAGUSD, USOIL, etc.

## 🚨 Troubleshooting

### Common Issues

1. **MT5 Connection Failed**
   - Verify credentials and server name
   - Check internet connection
   - Ensure MT5 allows API connections

2. **No Data Available**
   - Check symbol spelling
   - Verify market hours
   - Try different timeframe

3. **Linux Installation Issues**
   - Install Wine properly
   - Use Python 3.8+ with Wine
   - Try alternative MT5 packages

4. **TA-Lib Import Error**
   - Install TA-Lib binary
   - Use basic indicators (automatic fallback)
   - Check system dependencies

### Getting Help

- Check the `docs/troubleshooting.md` file
- Review MT5 connection logs
- Verify Python and package versions
- Test with demo account first

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## ⚠️ Disclaimer

This software is for educational and informational purposes only. It should not be considered financial advice. Trading cryptocurrencies and forex involves substantial risk and may not be suitable for all investors. Always consult with qualified financial professionals before making investment decisions.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/btc-analyzer/issues)
- **Documentation**: Check the `docs/` folder
- **Updates**: Watch the repository for updates

---

Made with ❤️ for the Bitcoin and crypto trading community