# Installation Guide - BTC Analyzer with MetaTrader 5

This guide provides detailed installation instructions for the Bitcoin Live Analyzer across different platforms.

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB free space
- **Internet**: Stable connection for real-time data
- **MetaTrader 5**: Terminal with active account

### Operating System Support
- ✅ **Windows 10/11** (Native MT5 support)
- ✅ **Linux** (Wine-based MT5 bridge)
- ✅ **macOS** (Wine-based MT5 bridge)
- ✅ **Google Colab** (Cloud environment)

## 🚀 Quick Installation Options

### Option 1: Google Colab (Recommended for Beginners)

**Advantages**: No local setup required, pre-configured environment

1. Open a new Google Colab notebook
2. Run the automatic setup:
```python
# Download and run setup script
!wget https://raw.githubusercontent.com/yourusername/btc-analyzer/main/scripts/colab_setup.py
!python colab_setup.py
```

3. Clone the repository:
```python
!git clone https://github.com/yourusername/btc-analyzer.git /content/btc-analyzer
```

4. Start the application:
```python
!python /content/start_btc_analyzer.py
```

### Option 2: Local Windows Installation

**Advantages**: Best performance, native MT5 support

1. **Install Python 3.8+**
   - Download from [python.org](https://python.org)
   - Ensure "Add to PATH" is checked during installation

2. **Install MetaTrader 5**
   - Download from your broker or [MetaQuotes](https://www.metatrader5.com/)
   - Create a demo account if needed

3. **Clone and setup the project**
```cmd
git clone https://github.com/yourusername/btc-analyzer.git
cd btc-analyzer
pip install -r requirements.txt
```

4. **Run the application**
```cmd
streamlit run src/btc_analyzer_app.py
```

### Option 3: Linux Installation

**Advantages**: Server deployment, automation-friendly

#### Ubuntu/Debian Setup

1. **Install system dependencies**
```bash
sudo apt update
sudo apt install python3 python3-pip git wine winetricks xvfb
```

2. **Setup Wine for MT5**
```bash
# Configure Wine environment
export WINEPREFIX="$HOME/.wine"
export WINEARCH="win32"
winecfg  # Set Windows version to Windows 10
```

3. **Install the application**
```bash
git clone https://github.com/yourusername/btc-analyzer.git
cd btc-analyzer
pip3 install -r requirements.txt
```

4. **Install MT5 Linux bridge**
```bash
pip3 install pymt5linux
# or alternatively
pip3 install mt5linux
```

5. **Run the application**
```bash
streamlit run src/btc_analyzer_app.py
```

## 🔧 Detailed Setup Instructions

### MetaTrader 5 Configuration

1. **Download MT5**
   - Windows: Download from broker or MetaQuotes
   - Linux: Install Windows version via Wine

2. **Create Trading Account**
   - Demo account (recommended for testing)
   - Live account (for real trading data)

3. **Enable API Access**
   - Open MT5 → Tools → Options
   - Go to "Expert Advisors" tab
   - Check "Allow automated trading"
   - Check "Allow DLL imports"
   - Click "OK"

4. **Get Connection Details**
   - Login: Your account number
   - Password: Your account password
   - Server: Your broker's server name

### Python Environment Setup

#### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv btc_analyzer_env

# Activate environment
# Windows:
btc_analyzer_env\Scripts\activate
# Linux/Mac:
source btc_analyzer_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Using Conda

```bash
# Create conda environment
conda create -n btc_analyzer python=3.9

# Activate environment
conda activate btc_analyzer

# Install dependencies
pip install -r requirements.txt
```

### TA-Lib Installation (Optional but Recommended)

TA-Lib provides advanced technical analysis indicators. Installation varies by platform:

#### Windows
```cmd
pip install TA-Lib
```

If the above fails:
```cmd
# Download appropriate wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
```

#### Linux (Ubuntu/Debian)
```bash
# Install TA-Lib dependencies
sudo apt install build-essential wget

# Download and compile TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install

# Install Python wrapper
pip install TA-Lib
```

#### macOS
```bash
# Using Homebrew
brew install ta-lib
pip install TA-Lib
```

## 🐳 Docker Installation (Advanced)

For containerized deployment:

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/btc_analyzer_app.py", "--server.headless", "true"]
```

2. **Build and run**
```bash
docker build -t btc-analyzer .
docker run -p 8501:8501 btc-analyzer
```

## 🔍 Verification and Testing

### 1. Test Python Installation
```python
python --version  # Should be 3.8+
```

### 2. Test Package Imports
```python
python -c "
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
print('✅ All core packages imported successfully')
"
```

### 3. Test MT5 Package
```python
python -c "
try:
    import MetaTrader5 as mt5
    print('✅ MetaTrader5 package imported successfully')
except ImportError as e:
    print(f'⚠️ MetaTrader5 import failed: {e}')
"
```

### 4. Test TA-Lib (Optional)
```python
python -c "
try:
    import talib
    print('✅ TA-Lib imported successfully')
except ImportError:
    print('⚠️ TA-Lib not available (basic indicators will be used)')
"
```

### 5. Run Application Test
```bash
cd btc-analyzer
python -c "
import sys
sys.path.append('src')
from mt5_integration import test_mt5_connection
test_mt5_connection()
"
```

## 🚨 Troubleshooting Common Issues

### Issue: MT5 Package Import Error
**Solution**: Try alternative packages
```bash
pip install pymt5linux  # For Linux
pip install mt5linux    # Alternative for Linux
```

### Issue: TA-Lib Installation Failed
**Solution**: Use basic indicators (automatic fallback)
```python
# The app will automatically use basic indicators if TA-Lib is not available
# No action required
```

### Issue: Streamlit Not Found
**Solution**: Install/reinstall Streamlit
```bash
pip uninstall streamlit
pip install streamlit>=1.28.0
```

### Issue: Wine Configuration Error (Linux)
**Solution**: Reconfigure Wine
```bash
winecfg
# Set Windows version to Windows 10
# Set Graphics to "Emulate a virtual desktop"
```

### Issue: Permission Denied (Linux)
**Solution**: Fix permissions
```bash
chmod +x scripts/colab_setup.py
chmod +x start_btc_analyzer.py
```

## 📊 Performance Optimization

### For Better Performance:
1. **Use SSD storage** for faster data access
2. **Allocate sufficient RAM** (4GB+ recommended)
3. **Close unnecessary applications** while running
4. **Use wired internet connection** for stable data feed
5. **Run on local machine** rather than cloud for lowest latency

### For Cloud Deployment:
1. **Use high-memory instances** (2GB+ RAM)
2. **Configure proper networking** for MT5 connectivity
3. **Set up automatic restarts** for reliability
4. **Monitor resource usage** and scale as needed

## 🔄 Updates and Maintenance

### Updating the Application
```bash
cd btc-analyzer
git pull origin main
pip install -r requirements.txt --upgrade
```

### Backing Up Configuration
- Export MT5 settings from terminal
- Save custom indicator configurations
- Backup any personal modifications

### Regular Maintenance
- Update Python packages monthly
- Check for new MT5 terminal versions
- Monitor performance and logs
- Test with demo account regularly

---

For additional help, check the [troubleshooting guide](troubleshooting.md) or create an issue on GitHub.