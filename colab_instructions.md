# Bitcoin Live Analyzer - Google Colab Instructions

## 📋 Step-by-Step Guide to Run the App in Google Colab

### Step 1: Upload Files to Colab
1. Open Google Colab (https://colab.research.google.com/)
2. Create a new notebook
3. Upload the following files to your Colab environment:
   - `colab_setup_fixed.py` (setup script)
   - `btc_live_analyzer.py` (main app file)
   - `requirements.txt` (dependencies)

### Step 2: Run the Setup Script
In a Colab cell, execute:
```python
exec(open('colab_setup_fixed.py').read())
```

This will:
- Install all required Python packages
- Set up TA-Lib (technical analysis library)
- Configure Streamlit
- Create the tunnel script for public access

### Step 3: Start the Application
After setup completes successfully, run:
```python
exec(open('run_tunnel.py').read())
```

This will:
- Start the Streamlit app
- Create a public ngrok tunnel
- Display a public URL to access your app

### Step 4: Access Your App
1. The script will output a public URL (e.g., `https://xxxxx.ngrok.io`)
2. Click on this URL to access your Bitcoin Live Analyzer
3. **Keep the Colab cell running** to maintain the connection

## 🔧 What the App Does

The Bitcoin Live Analyzer provides:
- **Real-time Bitcoin price data** from multiple exchanges
- **Technical indicators** (RSI, MACD, Bollinger Bands, etc.)
- **Machine learning predictions** using Random Forest and Gradient Boosting
- **Interactive charts** with Plotly
- **Trading signals** and market analysis
- **Risk assessment** and portfolio insights

## 📊 Features Available

### Full Version (with TA-Lib)
- 30+ technical indicators
- Advanced pattern recognition
- Professional trading signals

### Lite Version (without TA-Lib)
- Basic technical indicators (SMA, EMA, RSI, MACD)
- Price analysis and trends
- ML predictions

## 🚨 Important Notes

1. **Keep the cell running**: The app will stop if you interrupt the cell
2. **Ngrok tunnel**: The public URL changes each time you restart
3. **Free tier limits**: Colab has usage limits on free accounts
4. **Data updates**: The app fetches real-time data every few seconds

## 🔄 Restarting the App

If you need to restart:
1. Stop the current cell (Ctrl+C or interrupt button)
2. Run the tunnel script again:
   ```python
   exec(open('run_tunnel.py').read())
   ```

## ⚠️ Troubleshooting

### If you get ERR_NGROK_8012 (Connection Refused):
This means ngrok is working but Streamlit isn't running. Try these steps:

1. **Test your setup first**:
   ```python
   exec(open('test_app.py').read())
   ```

2. **Check if files are uploaded correctly**:
   - Ensure `btc_live_analyzer.py` exists in your Colab files
   - If not, upload it or run the setup script again

3. **Manual Streamlit test**:
   ```python
   import subprocess
   subprocess.run(['streamlit', 'run', 'btc_live_analyzer.py', '--server.port=8501'])
   ```

### If setup fails:
- Check your internet connection
- Restart the Colab runtime
- Try running the setup script again

### If the app doesn't load:
- Wait 30 seconds after starting (increased from 10)
- Check if the ngrok URL is accessible
- Ensure the cell is still running
- Run the test script to diagnose issues

### If you get package errors:
- The setup script will attempt to install missing packages
- Some packages may require system-level installation
- Try restarting the runtime and running setup again

## 🎯 Quick Start Commands

```python
# 1. Setup (run once)
exec(open('colab_setup_fixed.py').read())

# 2. Start app (run after setup)
exec(open('run_tunnel.py').read())
```

## 📱 Using the App

Once running, you can:
1. View real-time Bitcoin prices
2. Analyze technical indicators
3. Get ML-based price predictions
4. Monitor trading signals
5. Track market sentiment

The app updates automatically and provides a comprehensive dashboard for Bitcoin analysis.

---

**Happy Trading! 🚀📈**