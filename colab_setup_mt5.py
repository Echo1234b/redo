import subprocess
import sys
import os
import time

def run_command(command, description="Running command", check=True, shell=False):
    """Run a command with proper error handling"""
    print(f"🔄 {description}...")
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        
        if result.stdout:
            print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def install_metatrader5():
    """Install MetaTrader 5 Python package"""
    print("🔧 Installing MetaTrader 5 Python package...")
    
    # Install MetaTrader5 package
    packages = [
        "MetaTrader5",
        "pandas",
        "numpy"
    ]
    
    for package in packages:
        success = run_command(
            [sys.executable, "-m", "pip", "install", package],
            f"Installing {package}"
        )
        if not success:
            print(f"⚠️ Failed to install {package}, but continuing...")
    
    return True

def install_packages():
    """Install all required packages"""
    print("📦 Installing Python packages...")
    
    # Core packages for the app
    packages = [
        "streamlit==1.31.0",
        "pandas==2.0.3", 
        "numpy==1.24.3",
        "plotly==5.17.0",
        "requests==2.31.0",
        "scikit-learn==1.3.0",
        "joblib==1.3.2",
        "python-dateutil==2.8.2",
        "pytz==2023.3",
        "pyngrok"
    ]
    
    success_count = 0
    for package in packages:
        success = run_command(
            [sys.executable, "-m", "pip", "install", package],
            f"Installing {package}"
        )
        if success:
            success_count += 1
        else:
            print(f"⚠️ Failed to install {package}")
    
    print(f"📊 Successfully installed {success_count}/{len(packages)} packages")
    return success_count > len(packages) * 0.8  # 80% success rate

def install_talib_alternative():
    """Install TA-Lib using alternative methods"""
    
    print("🔧 Trying alternative TA-Lib installation methods...")
    
    # Method 1: Try installing TA-Lib from PyPI
    print("🔄 Method 1: Installing TA-Lib from PyPI...")
    success = run_command(
        [sys.executable, "-m", "pip", "install", "TA-Lib"],
        "Installing TA-Lib from PyPI",
        check=False
    )
    
    if success:
        print("✅ TA-Lib installed successfully from PyPI!")
        return True
    
    # Method 2: Try installing using conda-forge
    print("🔄 Method 2: Installing TA-Lib using conda...")
    success = run_command(
        ["conda", "install", "-c", "conda-forge", "ta-lib", "-y"],
        "Installing TA-Lib using conda",
        check=False
    )
    
    if success:
        print("✅ TA-Lib installed successfully using conda!")
        return True
    
    # Method 3: Try installing pre-compiled wheel
    print("🔄 Method 3: Installing pre-compiled TA-Lib wheel...")
    success = run_command(
        [sys.executable, "-m", "pip", "install", "--find-links", "https://github.com/cgohlke/talib-build/releases", "TA-Lib"],
        "Installing pre-compiled TA-Lib wheel",
        check=False
    )
    
    if success:
        print("✅ TA-Lib installed successfully from pre-compiled wheel!")
        return True
    
    print("⚠️ All TA-Lib installation methods failed. App will use basic indicators.")
    return False

def setup_streamlit():
    """Setup Streamlit configuration"""
    print("⚙️ Setting up Streamlit configuration...")
    
    # Create .streamlit directory
    streamlit_dir = os.path.expanduser("~/.streamlit")
    os.makedirs(streamlit_dir, exist_ok=True)
    
    # Create config.toml
    config_content = """
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
"""
    
    config_path = os.path.join(streamlit_dir, "config.toml")
    with open(config_path, "w") as f:
        f.write(config_content)
    
    print("✅ Streamlit configuration complete!")
    return True

def create_run_script(use_lite=False):
    """Create the run script for the app"""
    print("📝 Creating run script...")
    
    script_content = '''
import subprocess
import time
import socket
import sys
import os
from pyngrok import ngrok
import threading

def check_port(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(('127.0.0.1', port))
        return result == 0

def wait_for_service(port, timeout=60):
    """Wait for a service to be available on a port"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_port(port):
            return True
        time.sleep(1)
    return False

def run_streamlit():
    """Run Streamlit with proper error handling"""
    try:
        # Check if the main app file exists
        app_files = ['btc_live_analyzer_mt5.py', 'btc_live_analyzer.py']
        app_file = None
        
        for file in app_files:
            if os.path.exists(file):
                app_file = file
                break
        
        if not app_file:
            print("❌ Error: No app file found!")
            print("Looking for: btc_live_analyzer_mt5.py or btc_live_analyzer.py")
            return
        
        print(f"🔄 Starting Streamlit with {app_file}...")
        
        # Run streamlit with additional flags for Colab
        cmd = [
            'streamlit', 'run', app_file,
            '--server.port=8501',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--server.enableCORS=false',
            '--server.enableXsrfProtection=false'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor the process
        while process.poll() is None:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

def main():
    print("🚀 Starting Bitcoin Analyzer - MT5 Edition...")
    print("📋 Checking prerequisites...")
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'streamlit'])
    
    # Check if pyngrok is working
    try:
        print("✅ Pyngrok is available")
    except Exception as e:
        print(f"❌ Pyngrok error: {e}")
        return
    
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    print("⏳ Waiting for Streamlit to start...")
    
    # Wait for Streamlit to be ready
    if wait_for_service(8501, timeout=30):
        print("✅ Streamlit is running on port 8501")
    else:
        print("❌ Streamlit failed to start within 30 seconds")
        print("🔧 Troubleshooting:")
        print("   1. Check if the app file exists")
        print("   2. Verify all dependencies are installed")
        print("   3. Look for error messages above")
        return
    
    # Give it a bit more time to fully initialize
    time.sleep(5)
    
    try:
        # Create ngrok tunnel
        print("🌐 Creating public tunnel...")
        public_url = ngrok.connect(8501)
        print(f"\\n🎉 SUCCESS! Your MetaTrader Bitcoin Analyzer is running at:")
        print(f"🔗 {public_url}")
        print("\\n✨ Click the link above to access your app!")
        print("🔔 Keep this cell running to maintain the connection.")
        print("🛑 Press Ctrl+C to stop the app")
        
        # Keep the connection alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n🛑 Stopping...")
            ngrok.disconnect(public_url)
            print("✅ Tunnel disconnected")
            
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("🔧 Try restarting the kernel and running the setup again")

if __name__ == "__main__":
    main()
'''
    
    with open("run_tunnel_mt5.py", "w") as f:
        f.write(script_content)
    
    print("✅ Run script created successfully!")
    return True

def main():
    print("🚀 Bitcoin Live Analyzer - MT5 Edition Setup")
    print("=" * 50)
    
    try:
        # Install MetaTrader 5
        install_metatrader5()
        
        # Install packages
        talib_success = install_packages()
        
        # Try to install TA-Lib
        print("🎯 Installing TA-Lib (this is the tricky part)...")
        print("🔄 Installing TA-Lib standard method...")
        talib_success = install_talib_alternative()
        
        # Setup streamlit
        setup_streamlit()
        
        # Create run script
        create_run_script(use_lite=not talib_success)
        
        print("\n" + "=" * 50)
        if talib_success:
            print("✅ Full setup complete with TA-Lib and MetaTrader 5!")
            print("🎯 Run: exec(open('run_tunnel_mt5.py').read())")
        else:
            print("⚠️ Setup complete with lite version (no TA-Lib)")
            print("✅ MetaTrader 5 integration is ready!")
            print("🎯 Run: exec(open('run_tunnel_mt5.py').read())")
            print("📝 Note: Using basic indicators only")
        
        print("\n🔧 MetaTrader 5 Requirements:")
        print("1. Install MetaTrader 5 terminal on your computer")
        print("2. Have a demo or live trading account")
        print("3. Enable algorithmic trading in MT5")
        print("4. Use your MT5 login credentials in the app")
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        print("\n🔧 Try the manual installation steps:")
        print("1. pip install MetaTrader5")
        print("2. pip install streamlit pandas numpy plotly")
        print("3. Make sure MetaTrader 5 terminal is installed")

if __name__ == "__main__":
    main()