# MetaTrader5 Linux Installation Guide

## Problem Summary
The original MetaTrader5 Python package is **Windows-only** and cannot be installed directly on Linux systems. The error you encountered:

```
ERROR: Could not find a version that satisfies the requirement MetaTrader5 (from versions: none)
ERROR: No matching distribution found for MetaTrader5
```

This occurs because MetaTrader5 wheels are only built for Windows platforms (`win_amd64`).

## Solution Overview
To use MetaTrader5 on Linux, you need to use Wine (Windows compatibility layer) along with specialized Python packages that bridge the gap between Linux and the Windows-only MetaTrader5 API.

## Available Solutions

### Solution 1: pymt5linux (Recommended - Most Up-to-date)

**pymt5linux** is the most recent and actively maintained solution that supports Python 3.13.

#### Installation Steps:

1. **Create a virtual environment:**
   ```bash
   python3 -m venv mt5_env
   source mt5_env/bin/activate
   ```

2. **Install pymt5linux:**
   ```bash
   pip install pymt5linux
   ```

#### Prerequisites:
- Wine installed on your Linux system
- Python for Windows installed inside Wine
- MT5 software installed inside Wine
- MetaTrader5 package installed in your Wine Python installation

#### Usage:
```python
# import the package
from pymt5linux import MetaTrader5

# establish the connection
mt5 = MetaTrader5()

# or if you specified custom host and port:
mt5 = MetaTrader5(host="localhost", port=8001)

# Use the standard MT5 functions
mt5.initialize()
mt5.terminal_info()
# ... other MT5 operations
mt5.shutdown()
```

#### Running the server:
1. Open MT5 terminal in Wine
2. Run the MT5 server in Wine:
   ```bash
   python -m pymt5linux <path/to/python.exe>
   ```
   or with custom host and port:
   ```bash
   python -m pymt5linux --host localhost --port 8001 <path/to/python.exe>
   ```

### Solution 2: mt5linux (Alternative)

**mt5linux** is an older but still functional alternative.

#### Installation:
```bash
pip install mt5linux
```

#### Usage:
```python
from mt5linux import MetaTrader5

mt5 = MetaTrader5(
    # host = 'localhost' (default)
    # port = 18812       (default)
) 

mt5.initialize()
mt5.terminal_info()
mt5.copy_rates_from_pos('EURUSD', mt5.TIMEFRAME_M1, 0, 1000)
mt5.shutdown()
```

## Detailed Setup Guide

### Step 1: Install Wine
```bash
sudo apt update
sudo apt install wine
```

### Step 2: Install Python for Windows in Wine
```bash
cd ~/Downloads
wget https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe --no-check-certificate
wine python-3.8.0-amd64.exe
```
**Important:** Make sure to check "Add Python 3.8 to PATH" during installation.

### Step 3: Install MetaTrader5 in Wine
Follow the official MetaTrader 5 installation guide for Linux using Wine.

### Step 4: Install MetaTrader5 package in Wine Python
```bash
wine cmd
python -m pip install MetaTrader5
```

### Step 5: Install pymt5linux in both environments
In Wine Python:
```bash
wine cmd
python -m pip install pymt5linux
```

In Linux Python:
```bash
pip install pymt5linux
```

## Docker Alternative

For a simplified setup, you can use a Docker image with MT5 and x11/noVNC remote access. Check out [mt5docker](https://github.com/your-repo/mt5docker) for details.

## Troubleshooting

### Common Issues:

1. **Python not in PATH in Wine:**
   - Reinstall Python in Wine and ensure "Add Python to PATH" is checked
   - Manually add Python paths to Wine registry using `wine regedit`

2. **Missing DLL files:**
   - Download missing DLL files (like `ucrtbase.dll`) from DLL download sites
   - Place them in `~/.wine/drive_c/windows/system32`
   - Register them using `winecfg`

3. **Rust/Cargo errors during installation:**
   - Install Rust in Wine if required by dependencies
   - Alternative: Use older package versions that don't require Rust

## Testing Your Installation

Create a test script to verify your installation:

```python
from pymt5linux import MetaTrader5
import pandas as pd

# Create MetaTrader5 connection
mt5 = MetaTrader5()

try:
    # Initialize MT5 connection
    if not mt5.initialize():
        print("initialize() failed")
        quit()
    
    # Get account information
    account_info = mt5.account_info()
    if account_info is not None:
        print(f"Account balance: {account_info.balance}")
    
    # Get some market data
    rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M1, 0, 10)
    if rates is not None:
        df = pd.DataFrame(rates)
        print("Market data retrieved successfully:")
        print(df.head())
    
finally:
    # Shutdown MT5 connection
    mt5.shutdown()
```

## Important Notes

- **Test with DEMO accounts first** before using real trading accounts
- MetaTrader5 must be running in Wine for the Python connection to work
- All Python calls must run in the same Wine environment where MT5 is installed
- Consider using the most recent `pymt5linux` package as it supports Python 3.13 and incorporates recent MT5 software updates

## Performance Considerations

- Python scripts will run slower than native MQL5 programs due to interpretation overhead
- Wine adds additional overhead compared to native Windows execution
- Consider using background processes for long-running trading strategies

## Security

- Enable "Disable automatic trading via external Python API" in MT5 settings to protect accounts when using third-party libraries
- Always test thoroughly with demo accounts before live trading
- Keep your Wine and MT5 installations updated

## Resources

- [Official MetaTrader5 Python Documentation](https://www.mql5.com/en/docs/integration/python_metatrader5)
- [pymt5linux on PyPI](https://pypi.org/project/pymt5linux/)
- [mt5linux on PyPI](https://pypi.org/project/mt5linux/)
- [MetaTrader 5 Linux Installation Guide](https://www.mql5.com/en/articles/625)