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
        app_files = ['btc_live_analyzer.py', 'btc_live_analyzer_fixed.py']
        app_file = None
        
        for file in app_files:
            if os.path.exists(file):
                app_file = file
                break
        
        if not app_file:
            print("❌ Error: No app file found!")
            print("Looking for: btc_live_analyzer.py or btc_live_analyzer_fixed.py")
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
    print("🚀 Starting Bitcoin Analyzer...")
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
        print(f"\n🎉 SUCCESS! Your app is running at:")
        print(f"🔗 {public_url}")
        print("\n✨ Click the link above to access your Bitcoin Live Analyzer!")
        print("🔔 Keep this cell running to maintain the connection.")
        print("🛑 Press Ctrl+C to stop the app")
        
        # Keep the connection alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
            ngrok.disconnect(public_url)
            print("✅ Tunnel disconnected")
            
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("🔧 Try restarting the kernel and running the setup again")

if __name__ == "__main__":
    main()
