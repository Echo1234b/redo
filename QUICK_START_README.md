# 🚀 MetaTrader5 Linux Setup - Quick Start Guide

## ✅ What We've Accomplished

I've successfully set up your MetaTrader5 Python environment for Linux with the following components:

### 📦 Files Created:
1. **`mt5_env/`** - Python virtual environment with pymt5linux installed
2. **`MetaTrader5_Linux_Installation_Guide.md`** - Comprehensive documentation
3. **`MT5_Linux_Step_by_Step_Setup.md`** - Detailed step-by-step setup guide
4. **`setup_wine_mt5.sh`** - Automated Wine + MT5 setup script
5. **`install_mt5_linux.sh`** - Python environment setup script
6. **`test_mt5_connection.py`** - Connection test script
7. **`my_mt5_app.py`** - Sample trading application template

### 🔧 Current Status:
- ✅ Python 3.13 virtual environment created
- ✅ pymt5linux package installed and working
- ✅ Test scripts ready to use
- ⏳ Wine + MT5 setup pending (next step)

## 🎯 Immediate Next Steps

### Option 1: Automated Setup (Recommended)
Run the automated setup script:
```bash
./setup_wine_mt5.sh
```
This will:
- Install Wine and dependencies
- Download and install Python for Windows
- Download and install MetaTrader5 terminal
- Install all required Python packages in Wine
- Create startup scripts

### Option 2: Manual Setup
Follow the detailed guide in `MT5_Linux_Step_by_Step_Setup.md`

## 🏃‍♂️ Quick Test Run

After Wine setup is complete, test your installation:

### Terminal 1 - Start MT5 and Bridge:
```bash
# Start MT5 terminal
./start_mt5.sh

# In MT5: Create demo account and enable algorithmic trading

# Start bridge server (in a new terminal)
./start_mt5_bridge.sh
```

### Terminal 2 - Run Python App:
```bash
# Activate environment
source mt5_env/bin/activate

# Test connection
python test_mt5_connection.py

# Run your trading app
python my_mt5_app.py
```

## 📋 Expected Output

When everything works correctly, you should see:
```
🧪 Testing MetaTrader5 connection...
📡 Initializing connection to MT5...
✅ MT5 connection established!
📊 Terminal: MetaTrader 5
🏢 Company: MetaQuotes Ltd.
💰 Account: [Your Demo Account]
💵 Balance: 10000.00
💱 Currency: USD
📈 Testing market data retrieval...
📊 EURUSD - Bid: 1.xxxxx, Ask: 1.xxxxx
📊 Retrieved 10 historical rates for EURUSD
🎉 All tests passed! MT5 is ready for use.
```

## 🛠️ Architecture Overview

```
Linux System
├── Python 3.13 (Native Linux)
│   └── mt5_env/ (Virtual Environment)
│       └── pymt5linux (Bridge Client)
│
└── Wine (Windows Compatibility Layer)
    ├── Python 3.8 (Windows)
    │   ├── MetaTrader5 package
    │   └── pymt5linux server
    └── MetaTrader5 Terminal
```

## 🔄 Daily Workflow

Once set up, your daily workflow will be:

1. **Start MT5**: `./start_mt5.sh`
2. **Start Bridge**: `./start_mt5_bridge.sh` 
3. **Activate Python**: `source mt5_env/bin/activate`
4. **Run Your Code**: `python my_trading_strategy.py`

## 🚨 Important Notes

- **ALWAYS TEST WITH DEMO ACCOUNTS FIRST**
- Keep both terminals running (MT5 + bridge server)
- The bridge server must be running for Python connections to work
- MT5 terminal must be logged into an account
- Algorithmic trading must be enabled in MT5

## 📚 Documentation Reference

- **Complete Setup Guide**: `MT5_Linux_Step_by_Step_Setup.md`
- **Troubleshooting**: See the guides above
- **API Reference**: [Official MT5 Python Docs](https://www.mql5.com/en/docs/integration/python_metatrader5)

## 🆘 Need Help?

If you encounter issues:
1. Check the troubleshooting section in `MT5_Linux_Step_by_Step_Setup.md`
2. Verify all components are running:
   - `ps aux | grep terminal64` (MT5 should be running)
   - `ps aux | grep pymt5linux` (Bridge should be running)
3. Check Wine configuration: `winecfg`
4. Test Wine Python: `wine python --version`

## 🎉 You're Almost There!

The hardest part (figuring out the Linux compatibility) is done. Now you just need to run the Wine setup and you'll have a fully functional MetaTrader5 Python environment on Linux!

**Next command to run**: `./setup_wine_mt5.sh`