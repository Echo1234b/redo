#!/usr/bin/env python3
"""
BTC Analyzer - Application Launcher
Windows-optimized script to start the Bitcoin Live Analyzer with MetaTrader 5 integration
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def main():
    """Main launcher function"""
    print("🚀 Starting Bitcoin Live Analyzer...")
    print(f"💻 Platform: {platform.system()}")
    print("=" * 50)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    app_file = src_dir / "btc_analyzer_app.py"
    
    # Check if the app file exists
    if not app_file.exists():
        print("❌ Error: Application file not found!")
        print(f"Expected location: {app_file}")
        print("Please make sure you're running this from the project root directory.")
        return 1
    
    # Change to source directory
    os.chdir(src_dir)
    
    # Add source directory to Python path
    sys.path.insert(0, str(src_dir))
    
    # Construct Streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "btc_analyzer_app.py",
        "--server.headless", "false",
        "--server.port", "8501",
        "--server.address", "localhost"
    ]
    
    try:
        print("🌟 Starting Streamlit server...")
        print("📍 Application will open in your browser at: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the application")
        
        # Windows-specific messaging
        if platform.system() == "Windows":
            print("💡 Windows Tips:")
            print("   - If MT5 connection fails, make sure MT5 terminal is running")
            print("   - Enable 'Allow DLL imports' in MT5 settings")
            print("   - Try running as Administrator if needed")
        
        print("=" * 50)
        
        # Run the Streamlit app
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        return 0
    except FileNotFoundError:
        print("❌ Error: Streamlit not found!")
        print("Please install Streamlit: pip install streamlit")
        if platform.system() == "Windows":
            print("💡 Try running: windows_setup.bat")
        return 1
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        if platform.system() == "Windows":
            print("💡 Troubleshooting tips:")
            print("   1. Try running as Administrator")
            print("   2. Check Windows Defender/antivirus settings")
            print("   3. See WINDOWS_SETUP_GUIDE.md for help")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)