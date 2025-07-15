+import subprocess
+import sys
+import os
+import time
+
+def run_command(command, description="Running command", check=True, shell=False):
+    """Run a command with proper error handling"""
+    print(f"🔄 {description}...")
+    try:
+        if shell:
+            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
+        else:
+            result = subprocess.run(command, check=check, capture_output=True, text=True)
+        
+        if result.stdout:
+            print(f"✅ {description} completed successfully")
+        return True
+    except subprocess.CalledProcessError as e:
+        print(f"❌ {description} failed:")
+        print(f"Error: {e}")
+        if e.stdout:
+            print(f"STDOUT: {e.stdout}")
+        if e.stderr:
+            print(f"STDERR: {e.stderr}")
+        return False
+
+def install_talib_alternative():
+    """Install TA-Lib using alternative methods"""
+    
+    print("🔧 Trying alternative TA-Lib installation methods...")
+    
+    # Method 1: Try conda installation
+    print("📦 Attempting conda installation...")
+    if run_command([sys.executable, "-m", "pip", "install", "conda"], "Installing conda", check=False):
+        if run_command(["conda", "install", "-c", "conda-forge", "ta-lib", "-y"], "Installing TA-Lib via conda", check=False):
+            if run_command([sys.executable, "-m", "pip", "install", "TA-Lib"], "Installing TA-Lib Python wrapper", check=False):
+                return True
+    
+    # Method 2: Try pre-compiled wheel
+    print("🎯 Attempting pre-compiled wheel installation...")
+    wheel_commands = [
+        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "wheel"],
+        [sys.executable, "-m", "pip", "install", "TA-Lib", "--find-links", "https://pypi.org/simple/", "--trusted-host", "pypi.org"]
+    ]
+    
+    success = True
+    for cmd in wheel_commands:
+        if not run_command(cmd, f"Running {' '.join(cmd)}", check=False):
+            success = False
+            break
+    
+    if success:
+        return True
+    
+    # Method 3: Manual compilation with detailed steps
+    print("🛠️ Attempting manual compilation...")
+    
+    # Ensure we have all build dependencies
+    build_deps = [
+        ["apt-get", "update"],
+        ["apt-get", "install", "-y", "build-essential", "gcc", "g++", "make", "wget", "curl"],
+        ["apt-get", "install", "-y", "python3-dev", "python3-pip"],
+        ["apt-get", "install", "-y", "libblas-dev", "liblapack-dev", "gfortran"]
+    ]
+    
+    for cmd in build_deps:
+        run_command(cmd, f"Installing {' '.join(cmd[2:])}", check=False)
+    
+    # Download and compile TA-Lib
+    try:
+        print("📥 Downloading TA-Lib source...")
+        
+        # Clean up any previous attempts
+        run_command(["rm", "-rf", "ta-lib*"], "Cleaning previous attempts", check=False)
+        
+        # Download
+        if not run_command(["wget", "-q", "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"], "Downloading TA-Lib"):
+            return False
+        
+        # Extract
+        if not run_command(["tar", "-xzf", "ta-lib-0.4.0-src.tar.gz"], "Extracting TA-Lib"):
+            return False
+        
+        # Compile
+        original_dir = os.getcwd()
+        os.chdir("ta-lib")
+        
+        compile_commands = [
+            ["./configure", "--prefix=/usr", "--build=x86_64-linux-gnu"],
+            ["make", "-j2"],
+            ["make", "install"]
+        ]
+        
+        for cmd in compile_commands:
+            if not run_command(cmd, f"Compiling: {' '.join(cmd)}"):
+                os.chdir(original_dir)
+                return False
+        
+        os.chdir(original_dir)
+        
+        # Update library cache
+        run_command(["ldconfig"], "Updating library cache", check=False)
+        
+        # Install Python wrapper
+        time.sleep(2)  # Give system time to register the library
+        
+        if run_command([sys.executable, "-m", "pip", "install", "TA-Lib"], "Installing TA-Lib Python wrapper"):
+            return True
+            
+    except Exception as e:
+        print(f"❌ Manual compilation failed: {e}")
+        return False
+    
+    return False
+
+def install_packages():
+    """Install required packages for the Bitcoin analyzer"""
+    
+    print("🔧 Installing system dependencies...")
+    
+    # Update system
+    run_command(["apt-get", "update"], "Updating package lists")
+    
+    # Install basic dependencies first
+    basic_deps = [
+        "build-essential", "gcc", "g++", "make", "wget", "curl",
+        "python3-dev", "python3-pip", "pkg-config"
+    ]
+    
+    run_command(["apt-get", "install", "-y"] + basic_deps, "Installing basic dependencies")
+    
+    # Upgrade pip first
+    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")
+    
+    # Install Python packages (excluding TA-Lib initially)
+    print("📦 Installing Python packages...")
+    
+    packages_without_talib = [
+        "streamlit==1.31.0",
+        "pandas==2.0.3",
+        "numpy==1.24.3",
+        "plotly==5.17.0",
+        "requests==2.31.0",
+        "scikit-learn==1.3.0",
+        "joblib==1.3.2",
+        "python-dateutil==2.8.2",
+        "pytz==2023.3"
+    ]
+    
+    for package in packages_without_talib:
+        if not run_command([sys.executable, "-m", "pip", "install", package], f"Installing {package}", check=False):
+            print(f"⚠️ Warning: Failed to install {package}, continuing...")
+    
+    # Now try to install TA-Lib
+    print("🎯 Installing TA-Lib (this is the tricky part)...")
+    
+    # Try standard installation first
+    if run_command([sys.executable, "-m", "pip", "install", "TA-Lib==0.4.28"], "Installing TA-Lib standard method", check=False):
+        print("✅ TA-Lib installed successfully!")
+        return True
+    
+    # If that fails, try alternative methods
+    print("⚠️ Standard TA-Lib installation failed, trying alternatives...")
+    
+    if install_talib_alternative():
+        print("✅ TA-Lib installed via alternative method!")
+        return True
+    
+    print("❌ All TA-Lib installation methods failed.")
+    print("🔄 Creating fallback version without TA-Lib...")
+    
+    # Create a fallback version
+    create_fallback_version()
+    return False
+
+def create_fallback_version():
+    """Create a version that works without TA-Lib"""
+    
+    print("🛠️ Creating fallback version without TA-Lib...")
+    
+    fallback_code = '''
+import streamlit as st
+import pandas as pd
+import numpy as np
+import plotly.graph_objects as go
+import plotly.express as px
+from plotly.subplots import make_subplots
+import requests
+import time
+from datetime import datetime, timedelta
+import warnings
+warnings.filterwarnings('ignore')
+
+# Machine Learning imports
+from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
+from sklearn.preprocessing import StandardScaler
+from sklearn.model_selection import train_test_split
+from sklearn.metrics import accuracy_score
+from typing import Dict, List, Tuple
+
+# Simple technical indicators without TA-Lib
+def calculate_sma(data, window):
+    return data.rolling(window=window).mean()
+
+def calculate_ema(data, window):
+    return data.ewm(span=window).mean()
+
+def calculate_rsi(data, window=14):
+    delta = data.diff()
+    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
+    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
+    rs = gain / loss
+    return 100 - (100 / (1 + rs))
+
+def calculate_bollinger_bands(data, window=20, num_std=2):
+    rolling_mean = data.rolling(window=window).mean()
+    rolling_std = data.rolling(window=window).std()
+    upper_band = rolling_mean + (rolling_std * num_std)
+    lower_band = rolling_mean - (rolling_std * num_std)
+    return upper_band, rolling_mean, lower_band
+
+def calculate_macd(data, fast=12, slow=26, signal=9):
+    ema_fast = calculate_ema(data, fast)
+    ema_slow = calculate_ema(data, slow)
+    macd = ema_fast - ema_slow
+    macd_signal = calculate_ema(macd, signal)
+    macd_histogram = macd - macd_signal
+    return macd, macd_signal, macd_histogram
+
+# Set page config
+st.set_page_config(
+    page_title="Bitcoin Live Analyzer (Lite)",
+    page_icon="₿",
+    layout="wide",
+    initial_sidebar_state="expanded"
+)
+
+# Custom CSS
+st.markdown("""
+<style>
+    .main-header {
+        font-size: 3rem;
+        color: #f7931a;
+        text-align: center;
+        margin-bottom: 2rem;
+        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
+    }
+    .metric-container {
+        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
+        padding: 1rem;
+        border-radius: 10px;
+        margin: 0.5rem 0;
+        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
+    }
+</style>
+""", unsafe_allow_html=True)
+
+class BitcoinAnalyzerLite:
+    def __init__(self):
+        self.data = None
+        self.scaler = StandardScaler()
+        self.model = None
+        
+    def fetch_binance_data(self, symbol='BTCUSDT', interval='5m', limit=1000):
+        """Fetch live data from Binance API"""
+        try:
+            url = f"https://api.binance.com/api/v3/klines"
+            params = {
+                'symbol': symbol,
+                'interval': interval,
+                'limit': limit
+            }
+            
+            response = requests.get(url, params=params)
+            response.raise_for_status()
+            
+            data = response.json()
+            df = pd.DataFrame(data, columns=[
+                'timestamp', 'open', 'high', 'low', 'close', 'volume',
+                'close_time', 'quote_volume', 'count', 'taker_buy_volume',
+                'taker_buy_quote_volume', 'ignore'
+            ])
+            
+            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
+            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
+            df[numeric_columns] = df[numeric_columns].astype(float)
+            
+            return df
+            
+        except Exception as e:
+            st.error(f"Error fetching data: {str(e)}")
+            return None
+    
+    def calculate_indicators(self, df):
+        """Calculate basic technical indicators"""
+        if df is None or len(df) < 50:
+            return df
+        
+        # Simple indicators
+        df['sma_20'] = calculate_sma(df['close'], 20)
+        df['sma_50'] = calculate_sma(df['close'], 50)
+        df['ema_12'] = calculate_ema(df['close'], 12)
+        df['ema_26'] = calculate_ema(df['close'], 26)
+        
+        # RSI
+        df['rsi'] = calculate_rsi(df['close'])
+        
+        # Bollinger Bands
+        df['bb_upper'], df['bb_middle'], df['bb_lower'] = calculate_bollinger_bands(df['close'])
+        
+        # MACD
+        df['macd'], df['macd_signal'], df['macd_histogram'] = calculate_macd(df['close'])
+        
+        # Price change and volatility
+        df['price_change'] = df['close'].pct_change()
+        df['volatility'] = df['price_change'].rolling(window=20).std()
+        
+        return df
+
+def create_chart(df):
+    """Create interactive chart"""
+    fig = make_subplots(
+        rows=2, cols=1,
+        shared_xaxes=True,
+        vertical_spacing=0.05,
+        subplot_titles=('Price & Indicators', 'Volume'),
+        row_heights=[0.7, 0.3]
+    )
+    
+    # Candlestick
+    fig.add_trace(
+        go.Candlestick(
+            x=df['timestamp'],
+            open=df['open'],
+            high=df['high'],
+            low=df['low'],
+            close=df['close'],
+            name='BTCUSDT'
+        ),
+        row=1, col=1
+    )
+    
+    # Moving averages
+    if 'sma_20' in df.columns:
+        fig.add_trace(
+            go.Scatter(x=df['timestamp'], y=df['sma_20'], name='SMA 20', line=dict(color='orange')),
+            row=1, col=1
+        )
+        fig.add_trace(
+            go.Scatter(x=df['timestamp'], y=df['sma_50'], name='SMA 50', line=dict(color='purple')),
+            row=1, col=1
+        )
+    
+    # Volume
+    fig.add_trace(
+        go.Bar(x=df['timestamp'], y=df['volume'], name='Volume'),
+        row=2, col=1
+    )
+    
+    fig.update_layout(
+        title='Bitcoin Live Analysis (Lite Version)',
+        height=600,
+        template='plotly_dark'
+    )
+    
+    return fig
+
+def main():
+    st.markdown("<h1 class='main-header'>₿ Bitcoin Live Analyzer (Lite)</h1>", unsafe_allow_html=True)
+    st.info("ℹ️ This is the lite version without TA-Lib. Basic indicators only.")
+    
+    if 'analyzer' not in st.session_state:
+        st.session_state.analyzer = BitcoinAnalyzerLite()
+    
+    # Sidebar
+    st.sidebar.header("⚙️ Configuration")
+    auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh", value=True)
+    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 60)
+    data_limit = st.sidebar.slider("Data Points", 100, 1000, 500)
+    
+    # Fetch data
+    with st.spinner("Fetching Bitcoin data..."):
+        df = st.session_state.analyzer.fetch_binance_data(limit=data_limit)
+        
+        if df is not None:
+            df = st.session_state.analyzer.calculate_indicators(df)
+            
+            # Current price
+            current_price = df['close'].iloc[-1]
+            price_change = df['close'].iloc[-1] - df['close'].iloc[-2]
+            price_change_pct = (price_change / df['close'].iloc[-2]) * 100
+            
+            col1, col2, col3 = st.columns(3)
+            with col1:
+                st.metric("Price", f"${current_price:,.2f}", f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
+            with col2:
+                st.metric("Volume", f"{df['volume'].iloc[-1]/1000:.1f}K")
+            with col3:
+                if 'volatility' in df.columns:
+                    vol = df['volatility'].iloc[-1]
+                    st.metric("Volatility", f"{vol:.4f}")
+            
+            # Chart
+            chart = create_chart(df)
+            st.plotly_chart(chart, use_container_width=True)
+            
+            # Indicators
+            if 'rsi' in df.columns:
+                col1, col2 = st.columns(2)
+                with col1:
+                    rsi = df['rsi'].iloc[-1]
+                    st.metric("RSI", f"{rsi:.2f}")
+                with col2:
+                    if 'macd' in df.columns:
+                        macd = df['macd'].iloc[-1]
+                        st.metric("MACD", f"{macd:.4f}")
+    
+    if auto_refresh:
+        time.sleep(refresh_interval)
+        st.rerun()
+
+if __name__ == "__main__":
+    main()
+'''
+    
+    with open('btc_live_analyzer_lite.py', 'w') as f:
+        f.write(fallback_code)
+    
+    print("✅ Fallback version created as 'btc_live_analyzer_lite.py'")
+
+def setup_streamlit():
+    """Set up Streamlit configuration for Colab"""
+    
+    print("⚙️ Setting up Streamlit configuration...")
+    
+    config_dir = os.path.expanduser("~/.streamlit")
+    os.makedirs(config_dir, exist_ok=True)
+    
+    config_content = """
+[server]
+headless = true
+port = 8501
+enableCORS = false
+enableXsrfProtection = false
+
+[browser]
+gatherUsageStats = false
+"""
+    
+    with open(os.path.join(config_dir, "config.toml"), "w") as f:
+        f.write(config_content)
+    
+    print("✅ Streamlit configuration complete!")
+
+def create_run_script(use_lite=False):
+    """Create the run script"""
+    
+    filename = 'btc_live_analyzer_lite.py' if use_lite else 'btc_live_analyzer.py'
+    
+    tunnel_script = f"""
+import subprocess
+import time
+from pyngrok import ngrok
+import threading
+
+def run_streamlit():
+    subprocess.run(['streamlit', 'run', '{filename}', '--server.port=8501'])
+
+print("🚀 Starting Bitcoin Analyzer...")
+streamlit_thread = threading.Thread(target=run_streamlit)
+streamlit_thread.daemon = True
+streamlit_thread.start()
+
+time.sleep(10)
+
+public_url = ngrok.connect(8501)
+print(f"🌐 Bitcoin Analyzer: {{public_url}}")
+print("✨ Click the link above to access your app!")
+print("🔔 Keep this cell running to maintain connection.")
+
+try:
+    while True:
+        time.sleep(1)
+except KeyboardInterrupt:
+    print("🛑 Stopping...")
+    ngrok.disconnect(public_url)
+"""
+    
+    with open("run_tunnel.py", "w") as f:
+        f.write(tunnel_script)
+
+def main():
+    print("🚀 Bitcoin Live Analyzer - FIXED Setup")
+    print("=" * 50)
+    
+    try:
+        # Install pyngrok first (usually works)
+        run_command([sys.executable, "-m", "pip", "install", "pyngrok"], "Installing pyngrok")
+        
+        # Try to install packages
+        talib_success = install_packages()
+        
+        # Setup streamlit
+        setup_streamlit()
+        
+        # Create run script
+        create_run_script(use_lite=not talib_success)
+        
+        if talib_success:
+            print("\n✅ Full setup complete with TA-Lib!")
+            print("🎯 Run: exec(open('run_tunnel.py').read())")
+        else:
+            print("\n⚠️ Setup complete with lite version (no TA-Lib)")
+            print("🎯 Run: exec(open('run_tunnel.py').read())")
+            print("📝 Note: Using basic indicators only")
+        
+    except Exception as e:
+        print(f"❌ Setup failed: {str(e)}")
+        print("\n🔧 Try the manual installation steps from the README")
+
+if __name__ == "__main__":
+    main()
