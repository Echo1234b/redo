# MetaTrader5 Linux: Complete Step-by-Step Setup and Connection Guide

## Overview
This guide will walk you through every step needed to run MetaTrader5 with Python on Linux, from initial setup to making your first connection.

## Phase 1: Install Wine and Dependencies

### Step 1: Install Wine
```bash
# Update package list
sudo apt update

# Install Wine
sudo apt install wine

# Initialize Wine (creates ~/.wine directory)
winecfg
```
**Note**: A Wine configuration window will open. Set Windows version to "Windows 10" and click OK.

### Step 2: Install required Wine components
```bash
# Install additional Windows libraries
sudo apt install winetricks

# Install Visual C++ redistributables (needed for MT5)
winetricks vcrun2019
```

## Phase 2: Install Python for Windows in Wine

### Step 3: Download and Install Python for Windows
```bash
# Create downloads directory
mkdir -p ~/Downloads
cd ~/Downloads

# Download Python 3.8 for Windows (compatible with MT5)
wget https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe

# Install Python in Wine
wine python-3.8.10-amd64.exe
```

**⚠️ IMPORTANT**: During installation:
- ✅ Check "Add Python 3.8 to PATH"
- ✅ Check "Install for all users"
- Choose "Customize installation" and install all optional features

### Step 4: Verify Wine Python Installation
```bash
# Test Wine Python
wine cmd
python --version
# Should show: Python 3.8.10

# Test pip
python -m pip --version
# Should show pip version

# Exit Wine command prompt
exit
```

## Phase 3: Install MetaTrader5 Terminal in Wine

### Step 5: Download and Install MT5 Terminal
```bash
cd ~/Downloads

# Download MT5 installer
wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe

# Install MT5 in Wine
wine mt5setup.exe
```

**During installation**:
- Accept license agreement
- Choose installation directory (default is fine)
- Complete installation

### Step 6: Configure MT5 Terminal
```bash
# Launch MT5 terminal
wine ~/.wine/drive_c/Program\ Files/MetaTrader\ 5/terminal64.exe
```

**In MT5 terminal**:
1. Click "File" → "Open an Account"
2. Choose a broker or select "MetaQuotes Demo"
3. Create a demo account for testing
4. Enable "Algorithmic Trading" button in the toolbar (should be green)

## Phase 4: Install MetaTrader5 Python Package in Wine

### Step 7: Install MetaTrader5 in Wine Python
```bash
# Open Wine command prompt
wine cmd

# Install MetaTrader5 package
python -m pip install MetaTrader5

# Verify installation
python -c "import MetaTrader5; print('MT5 installed successfully')"

# Exit Wine command prompt
exit
```

## Phase 5: Install pymt5linux Bridge

### Step 8: Install pymt5linux in Wine Python
```bash
# In Wine command prompt
wine cmd
python -m pip install pymt5linux
exit
```

### Step 9: Activate Linux Virtual Environment
```bash
# Activate the environment we created earlier
source mt5_env/bin/activate

# Verify pymt5linux is installed
python -c "from pymt5linux import MetaTrader5; print('pymt5linux ready!')"
```

## Phase 6: Test the Connection

### Step 10: Create a Test Script
```bash
# Create test script
cat > test_mt5_connection.py << 'EOF'
#!/usr/bin/env python3

from pymt5linux import MetaTrader5
import pandas as pd
import time

def test_mt5_connection():
    print("🧪 Testing MetaTrader5 connection...")
    
    # Create MetaTrader5 instance
    mt5 = MetaTrader5()
    
    try:
        # Initialize connection
        print("📡 Initializing connection to MT5...")
        if not mt5.initialize():
            print("❌ Failed to initialize MT5 connection")
            print("Error:", mt5.last_error())
            return False
        
        print("✅ MT5 connection established!")
        
        # Get terminal info
        terminal_info = mt5.terminal_info()
        if terminal_info:
            print(f"📊 Terminal: {terminal_info.name}")
            print(f"🏢 Company: {terminal_info.company}")
            print(f"📍 Path: {terminal_info.path}")
        
        # Get account info
        account_info = mt5.account_info()
        if account_info:
            print(f"💰 Account: {account_info.login}")
            print(f"💵 Balance: {account_info.balance}")
            print(f"💱 Currency: {account_info.currency}")
        
        # Test market data
        print("📈 Testing market data retrieval...")
        symbol = "EURUSD"
        
        # Get current price
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            print(f"📊 {symbol} - Bid: {tick.bid}, Ask: {tick.ask}")
        
        # Get historical data
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 10)
        if rates is not None and len(rates) > 0:
            print(f"📊 Retrieved {len(rates)} historical rates for {symbol}")
            df = pd.DataFrame(rates)
            print("Latest rates:")
            print(df[['time', 'open', 'high', 'low', 'close']].tail(3))
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
        
    finally:
        # Cleanup
        mt5.shutdown()
        print("🔒 MT5 connection closed")

if __name__ == "__main__":
    success = test_mt5_connection()
    if success:
        print("\n🎉 All tests passed! MT5 is ready for use.")
    else:
        print("\n💥 Tests failed. Check the setup steps above.")
EOF

chmod +x test_mt5_connection.py
```

## Phase 7: Run the Application

### Step 11: Start the MT5 Server Bridge
Open a **first terminal** and start the MT5 server:

```bash
# Make sure MT5 terminal is running in Wine first
wine ~/.wine/drive_c/Program\ Files/MetaTrader\ 5/terminal64.exe &

# Wait a few seconds for MT5 to load, then start the bridge server
sleep 10

# Start the pymt5linux server (in Wine)
wine cmd
cd C:\
python -m pymt5linux C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python38\python.exe

# Leave this terminal running
```

### Step 12: Run Your Python Application
Open a **second terminal** and run your Python code:

```bash
# Navigate to your workspace
cd /workspace

# Activate virtual environment
source mt5_env/bin/activate

# Run the test script
python test_mt5_connection.py
```

## Phase 8: Create Your Trading Application

### Step 13: Basic Trading Script Template
```bash
cat > my_mt5_app.py << 'EOF'
#!/usr/bin/env python3

from pymt5linux import MetaTrader5
import pandas as pd
import time
from datetime import datetime

class MT5TradingApp:
    def __init__(self, host="localhost", port=8001):
        self.mt5 = MetaTrader5(host=host, port=port)
        self.connected = False
    
    def connect(self):
        """Establish connection to MT5"""
        try:
            if not self.mt5.initialize():
                print(f"❌ Connection failed: {self.mt5.last_error()}")
                return False
            
            self.connected = True
            print("✅ Connected to MetaTrader5")
            
            # Print account info
            account = self.mt5.account_info()
            if account:
                print(f"📊 Account: {account.login}")
                print(f"💰 Balance: {account.balance} {account.currency}")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_market_data(self, symbol="EURUSD", timeframe=None, count=100):
        """Get historical market data"""
        if not self.connected:
            print("❌ Not connected to MT5")
            return None
        
        if timeframe is None:
            timeframe = self.mt5.TIMEFRAME_M1
        
        try:
            rates = self.mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            if rates is not None:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                return df
            return None
            
        except Exception as e:
            print(f"❌ Error getting market data: {e}")
            return None
    
    def get_current_price(self, symbol="EURUSD"):
        """Get current bid/ask prices"""
        if not self.connected:
            return None
        
        try:
            tick = self.mt5.symbol_info_tick(symbol)
            if tick:
                return {"bid": tick.bid, "ask": tick.ask, "time": tick.time}
            return None
            
        except Exception as e:
            print(f"❌ Error getting price: {e}")
            return None
    
    def place_order(self, symbol, order_type, volume, price=None, sl=None, tp=None):
        """Place a trading order (demo only!)"""
        if not self.connected:
            print("❌ Not connected to MT5")
            return False
        
        # This is a template - implement based on your trading strategy
        print(f"📝 Order template: {order_type} {volume} {symbol} at {price}")
        print("⚠️ Implement actual order placement logic here")
        return True
    
    def disconnect(self):
        """Close connection to MT5"""
        if self.connected:
            self.mt5.shutdown()
            self.connected = False
            print("🔒 Disconnected from MT5")

def main():
    # Create trading app instance
    app = MT5TradingApp()
    
    # Connect to MT5
    if not app.connect():
        return
    
    try:
        # Example: Get market data
        print("\n📈 Getting market data...")
        data = app.get_market_data("EURUSD", count=20)
        if data is not None:
            print(f"📊 Retrieved {len(data)} candles")
            print(data[['time', 'open', 'high', 'low', 'close']].tail())
        
        # Example: Get current price
        print("\n💱 Current prices:")
        price = app.get_current_price("EURUSD")
        if price:
            print(f"EURUSD - Bid: {price['bid']}, Ask: {price['ask']}")
        
        # Add your trading logic here
        print("\n🤖 Add your trading strategy here...")
        
    except KeyboardInterrupt:
        print("\n⏹️ Stopping application...")
    
    finally:
        app.disconnect()

if __name__ == "__main__":
    main()
EOF

chmod +x my_mt5_app.py
```

### Step 14: Run Your Trading Application
```bash
# Make sure MT5 bridge server is running (from Step 11)
# Then run your app:
python my_mt5_app.py
```

## Troubleshooting Common Issues

### Issue 1: "Connection refused" error
**Solution:**
```bash
# Check if MT5 terminal is running
ps aux | grep terminal64

# Check if bridge server is running
ps aux | grep pymt5linux

# Restart both if needed
```

### Issue 2: "No module named MetaTrader5" in Wine
**Solution:**
```bash
wine cmd
python -m pip install --upgrade MetaTrader5
```

### Issue 3: MT5 shows "Algorithmic trading disabled"
**Solution:**
1. In MT5 terminal, click Tools → Options
2. Go to "Expert Advisors" tab
3. Check "Allow algorithmic trading"
4. Check "Allow DLL imports"
5. Restart MT5

### Issue 4: Permission denied errors
**Solution:**
```bash
# Fix Wine permissions
sudo chown -R $USER:$USER ~/.wine
```

## Quick Start Commands (After Setup)

Once everything is set up, use these commands to start working:

```bash
# Terminal 1: Start MT5 and bridge
wine ~/.wine/drive_c/Program\ Files/MetaTrader\ 5/terminal64.exe &
sleep 10
wine cmd
python -m pymt5linux C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python38\python.exe

# Terminal 2: Run your Python app
source mt5_env/bin/activate
python my_mt5_app.py
```

## Security Notes

⚠️ **IMPORTANT SECURITY WARNINGS:**
- Always test with DEMO accounts first
- Never commit real account credentials to code
- Use environment variables for sensitive data
- Enable MT5's "Disable automatic trading via external Python API" for additional safety

## Next Steps

1. Test the connection with the provided scripts
2. Modify `my_mt5_app.py` to implement your trading strategy
3. Add proper error handling and logging
4. Implement risk management features
5. Test thoroughly with demo accounts before live trading

Your MetaTrader5 Python environment is now ready for development! 🚀