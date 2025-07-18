# Bitcoin Analyzer - Windows Setup Guide

## 🚀 Quick Start for Windows

### Option 1: Automated Setup (Recommended)
1. **Download the app** to your computer
2. **Run the setup script**: Double-click `windows_setup.bat`
3. **Start the app**: Run `python run_app.py`
4. **Open your browser** to http://localhost:8501

### Option 2: Manual Setup
```bash
# Install core dependencies
pip install streamlit pandas numpy plotly scikit-learn

# Install Windows-specific packages
pip install pywin32 wmi

# Install MetaTrader5 (for live trading)
pip install MetaTrader5

# Install TA-Lib (for advanced indicators)
pip install --find-links=https://github.com/mrjbq7/ta-lib/releases/latest --prefer-binary TA-Lib
```

## 📋 Prerequisites

### Required Software
- **Python 3.8+** - Download from [python.org](https://python.org)
- **Git** (optional) - For cloning the repository
- **Visual C++ Build Tools** (for TA-Lib) - [Download here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Optional Software
- **MetaTrader 5 Terminal** - Download from [MetaQuotes](https://www.metatrader5.com/)

## 🔧 Installation Steps

### Step 1: Install Python
1. Download Python 3.8+ from [python.org](https://python.org)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation: Open CMD and run `python --version`

### Step 2: Install Visual C++ Build Tools (for TA-Lib)
1. Download from [Microsoft](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Install "C++ build tools" workload
3. Restart your computer after installation

### Step 3: Install the Application
```bash
# Clone or download the repository
git clone <repository-url>
cd bitcoin-analyzer

# Run automated setup
windows_setup.bat

# OR install manually
pip install -r requirements.txt
```

### Step 4: Install MetaTrader 5 (Optional)
1. Download MT5 from [MetaQuotes](https://www.metatrader5.com/)
2. Install and create a demo account (or use your live account)
3. **Important Settings**:
   - Go to Tools → Options → Expert Advisors
   - Check "Allow DLL imports"
   - Check "Allow WebRequest for listed URLs"

## 🚨 Troubleshooting

### Problem: "MetaTrader5 module not found"
**Solution:**
```bash
pip install MetaTrader5
```
If this fails:
- Ensure MT5 terminal is installed
- Try running CMD as Administrator
- The app will work in demo mode without MT5

### Problem: "TA-Lib installation failed"
**Solutions:**
1. **Install Visual C++ Build Tools first**
2. **Try pre-compiled wheel:**
   ```bash
   pip install --find-links=https://github.com/mrjbq7/ta-lib/releases/latest --prefer-binary TA-Lib
   ```
3. **Alternative method:**
   ```bash
   pip install TA-Lib-binary
   ```
4. **If all else fails:** The app has built-in fallback indicators

### Problem: "MT5 connection failed"
**Check these settings:**
1. **MT5 Terminal is running**
2. **Allow DLL imports** is enabled in MT5 settings
3. **Windows Defender/Antivirus** isn't blocking MT5
4. **Run as Administrator** if needed
5. **Firewall settings** allow MT5 connections

### Problem: "Streamlit not found"
**Solution:**
```bash
pip install streamlit
```

### Problem: "Permission denied" errors
**Solutions:**
1. **Run CMD as Administrator**
2. **Use virtual environment:**
   ```bash
   python -m venv btc_env
   btc_env\Scripts\activate
   pip install -r requirements.txt
   ```

## 🎮 Demo Mode vs Live Mode

### Demo Mode (Always Available)
- ✅ Works without any external dependencies
- ✅ Simulated Bitcoin data
- ✅ All technical analysis features
- ✅ Machine learning predictions
- ✅ Interactive charts

### Live Mode (Requires MT5)
- ✅ Real-time market data
- ✅ Multiple trading symbols
- ✅ Live price feeds
- ✅ Account information
- ✅ Trading capabilities

## 📊 Feature Comparison

| Feature | Demo Mode | Live Mode (MT5) |
|---------|-----------|-----------------|
| Technical Analysis | ✅ | ✅ |
| Price Predictions | ✅ | ✅ |
| Interactive Charts | ✅ | ✅ |
| Real-time Data | ❌ | ✅ |
| Multiple Symbols | Limited | ✅ |
| Account Info | ❌ | ✅ |
| Live Trading | ❌ | ✅ |

## 🔍 Verifying Installation

### Check Python
```bash
python --version
# Should show Python 3.8+
```

### Check Core Packages
```bash
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import numpy; print('Numpy:', numpy.__version__)"
```

### Check Optional Packages
```bash
python -c "import MetaTrader5; print('MT5: Available')"
python -c "import talib; print('TA-Lib: Available')"
```

## 🚀 Running the Application

### Method 1: Simple Start
```bash
python run_app.py
```

### Method 2: Direct Streamlit
```bash
streamlit run src/btc_analyzer_app.py
```

### Method 3: With Custom Port
```bash
streamlit run src/btc_analyzer_app.py --server.port 8502
```

## 💡 Tips for Windows Users

### Performance Optimization
1. **Close unnecessary programs** before running
2. **Use SSD storage** for better performance
3. **Ensure sufficient RAM** (4GB+ recommended)
4. **Update Windows** for latest compatibility

### Security Settings
1. **Add Python to Windows Defender exclusions**
2. **Allow MT5 through Windows Firewall**
3. **Run as Administrator** if permission issues occur

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv btc_analyzer_env

# Activate (Windows)
btc_analyzer_env\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run app
python run_app.py
```

## 📞 Getting Help

### If the app doesn't work:
1. **Check the error message** in the terminal
2. **Try demo mode first** - it should always work
3. **Check Windows Event Viewer** for system errors
4. **Restart your computer** and try again

### Common Error Messages:
- `ModuleNotFoundError`: Package not installed → Run `pip install <package>`
- `Permission denied`: → Run as Administrator
- `MT5 initialization failed`: → Check MT5 settings and restart terminal
- `Port already in use`: → Use different port with `--server.port 8502`

## 🎯 Success Indicators

You'll know everything is working when:
- ✅ App opens in browser at http://localhost:8501
- ✅ Status shows "Platform: Windows"
- ✅ TA-Lib status shows available (green) or fallback (yellow)
- ✅ MT5 status shows available (green) or demo mode (blue)
- ✅ Charts and data load without errors

## 🔄 Updates and Maintenance

### Updating the App
```bash
git pull  # If using git
pip install -r requirements.txt --upgrade
```

### Keeping Packages Updated
```bash
pip install --upgrade streamlit pandas numpy plotly scikit-learn
```

---

**Need help?** Check the error messages in the terminal and refer to this guide. The app is designed to work even if some components fail to install!