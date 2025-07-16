
import subprocess
import time
from pyngrok import ngrok
import threading

def run_streamlit():
    subprocess.run(['streamlit', 'run', 'btc_live_analyzer.py', '--server.port=8501'])

print("🚀 Starting Bitcoin Analyzer...")
streamlit_thread = threading.Thread(target=run_streamlit)
streamlit_thread.daemon = True
streamlit_thread.start()

time.sleep(10)

public_url = ngrok.connect(8501)
print(f"🌐 Bitcoin Analyzer: {public_url}")
print("✨ Click the link above to access your app!")
print("🔔 Keep this cell running to maintain connection.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("🛑 Stopping...")
    ngrok.disconnect(public_url)
