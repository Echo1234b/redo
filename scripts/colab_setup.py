#!/usr/bin/env python3
"""
Google Colab Setup Script for BTC Analyzer with MetaTrader 5
This script sets up the complete environment for running the BTC analyzer in Colab
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def run_command(command, description="Running command", check=True, shell=False):
    """Run a command with proper error handling"""
    print(f"🔄 {description}...")
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        
        if result.stdout:
            print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def install_system_dependencies():
    """Install system-level dependencies required for MT5"""
    print("🔧 Installing system dependencies...")
    
    commands = [
        ["apt-get", "update"],
        ["apt-get", "install", "-y", "wine", "winetricks", "xvfb"],
        ["apt-get", "install", "-y", "python3-dev", "build-essential"],
        ["apt-get", "install", "-y", "libffi-dev", "libssl-dev"],
        ["apt-get", "clean"]
    ]
    
    for cmd in commands:
        run_command(cmd, f"Running: {' '.join(cmd)}")

def install_python_packages():
    """Install Python packages for the BTC analyzer"""
    print("📦 Installing Python packages...")
    
    # Core packages for the application
    packages = [
        "streamlit>=1.28.0",
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "plotly>=5.17.0",
        "scikit-learn>=1.3.0",
        "requests>=2.31.0",
        "python-dateutil>=2.8.0",
        "pytz>=2023.3"
    ]
    
    # Install core packages
    for package in packages:
        run_command(
            [sys.executable, "-m", "pip", "install", package],
            f"Installing {package}"
        )
    
    # Try to install TA-Lib (may fail, but we have fallbacks)
    print("🔄 Attempting to install TA-Lib...")
    talib_success = run_command(
        [sys.executable, "-m", "pip", "install", "TA-Lib"],
        "Installing TA-Lib",
        check=False
    )
    
    if not talib_success:
        print("⚠️ TA-Lib installation failed, will use basic indicators")
    
    return True

def install_mt5_linux():
    """Install MT5 Linux bridge"""
    print("🔄 Installing MT5 Linux support...")
    
    # Try multiple MT5 Linux packages
    mt5_packages = [
        "pymt5linux",
        "mt5linux"
    ]
    
    mt5_installed = False
    for package in mt5_packages:
        success = run_command(
            [sys.executable, "-m", "pip", "install", package],
            f"Installing {package}",
            check=False
        )
        if success:
            mt5_installed = True
            break
    
    if not mt5_installed:
        print("⚠️ Failed to install MT5 Linux packages")
        print("🔧 Installing MetaTrader5 package directly...")
        run_command(
            [sys.executable, "-m", "pip", "install", "MetaTrader5"],
            "Installing MetaTrader5 package",
            check=False
        )
    
    return True

def setup_wine_environment():
    """Setup Wine environment for MT5"""
    print("🍷 Setting up Wine environment...")
    
    # Set Wine environment variables
    wine_env = {
        'WINEPREFIX': '/content/.wine',
        'WINEARCH': 'win32',
        'DISPLAY': ':0'
    }
    
    for key, value in wine_env.items():
        os.environ[key] = value
    
    # Initialize Wine (minimal setup)
    run_command(
        ["winecfg"],
        "Initializing Wine configuration",
        check=False,
        shell=True
    )
    
    return True

def download_mt5_terminal():
    """Download MT5 terminal for Wine"""
    print("📥 Downloading MT5 terminal...")
    
    mt5_url = "https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe"
    mt5_file = "/content/mt5setup.exe"
    
    try:
        response = requests.get(mt5_url, stream=True)
        response.raise_for_status()
        
        with open(mt5_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ MT5 terminal downloaded")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download MT5 terminal: {e}")
        return False

def create_test_script():
    """Create a test script to verify installation"""
    test_script = """
import sys
print("🧪 Testing BTC Analyzer Installation")
print("=" * 50)

# Test imports
try:
    import pandas as pd
    print("✅ Pandas imported successfully")
except ImportError as e:
    print(f"❌ Pandas import failed: {e}")

try:
    import numpy as np
    print("✅ NumPy imported successfully")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")

try:
    import plotly.graph_objects as go
    print("✅ Plotly imported successfully")
except ImportError as e:
    print(f"❌ Plotly import failed: {e}")

try:
    import streamlit as st
    print("✅ Streamlit imported successfully")
except ImportError as e:
    print(f"❌ Streamlit import failed: {e}")

try:
    from sklearn.ensemble import RandomForestClassifier
    print("✅ Scikit-learn imported successfully")
except ImportError as e:
    print(f"❌ Scikit-learn import failed: {e}")

# Test TA-Lib
try:
    import talib
    print("✅ TA-Lib imported successfully")
    HAS_TALIB = True
except ImportError:
    print("⚠️ TA-Lib not available (will use basic indicators)")
    HAS_TALIB = False

# Test MT5
try:
    import MetaTrader5 as mt5
    print("✅ MetaTrader5 package imported successfully")
    MT5_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ MetaTrader5 import failed: {e}")
    MT5_AVAILABLE = False

print("=" * 50)
print("🎯 Installation Summary:")
print(f"   TA-Lib Available: {HAS_TALIB}")
print(f"   MT5 Package Available: {MT5_AVAILABLE}")
print("=" * 50)
"""
    
    with open("/content/test_installation.py", "w") as f:
        f.write(test_script)
    
    print("✅ Test script created at /content/test_installation.py")

def create_launcher_script():
    """Create a launcher script for the BTC analyzer"""
    launcher_script = """#!/usr/bin/env python3
'''
BTC Analyzer Launcher for Google Colab
Run this script to start the BTC analyzer application
'''

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Starting BTC Analyzer...")
    
    # Set up paths
    src_path = Path("/content/btc-analyzer/src")
    if not src_path.exists():
        print("❌ BTC Analyzer source code not found!")
        print("Please make sure you've cloned the repository to /content/btc-analyzer/")
        return
    
    # Change to source directory
    os.chdir(src_path)
    
    # Add source to Python path
    sys.path.insert(0, str(src_path))
    
    # Start Streamlit app
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", "btc_analyzer_app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        print("🌟 Starting Streamlit server...")
        print("📍 The app will be available at the Colab external URL")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
"""
    
    with open("/content/start_btc_analyzer.py", "w") as f:
        f.write(launcher_script)
    
    # Make it executable
    os.chmod("/content/start_btc_analyzer.py", 0o755)
    print("✅ Launcher script created at /content/start_btc_analyzer.py")

def main():
    """Main setup function"""
    print("🚀 BTC Analyzer - Colab Setup Script")
    print("=" * 50)
    
    # Check if running in Colab
    try:
        import google.colab
        print("✅ Running in Google Colab")
    except ImportError:
        print("⚠️ Not running in Google Colab, continuing anyway...")
    
    # Install system dependencies
    install_system_dependencies()
    
    # Install Python packages
    install_python_packages()
    
    # Install MT5 Linux support
    install_mt5_linux()
    
    # Setup Wine environment
    setup_wine_environment()
    
    # Download MT5 terminal (optional)
    download_mt5_terminal()
    
    # Create test and launcher scripts
    create_test_script()
    create_launcher_script()
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("")
    print("📋 Next steps:")
    print("1. Run the test script: python /content/test_installation.py")
    print("2. Clone your BTC analyzer repository to /content/btc-analyzer/")
    print("3. Start the analyzer: python /content/start_btc_analyzer.py")
    print("")
    print("💡 Tips:")
    print("- Use a demo MT5 account for testing")
    print("- Ensure your broker supports the symbols you want to analyze")
    print("- The Wine setup is for running MT5 terminal if needed")
    print("")

if __name__ == "__main__":
    main()