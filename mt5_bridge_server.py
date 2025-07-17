#!/usr/bin/env python3
"""
MetaTrader5 Bridge Server for Google Colab Integration

This script creates a simple HTTP bridge between Google Colab and your local MetaTrader5 installation.
It exposes MT5 functionality through REST API endpoints that can be accessed from Colab via ngrok.

Prerequisites:
1. MetaTrader5 terminal running and logged in
2. MetaTrader5 Python package installed: pip install MetaTrader5
3. Flask installed: pip install flask
4. ngrok installed and configured

Usage:
1. Start this script: python mt5_bridge_server.py
2. In another terminal: ngrok http 5000
3. Use the ngrok URL in your Colab notebook

Security Notes:
- This server is for development/testing only
- Use demo accounts only
- Don't expose to public internet without authentication
- Monitor ngrok URLs for security
"""

from flask import Flask, jsonify, request, render_template_string
import MetaTrader5 as mt5
import pandas as pd
import json
from datetime import datetime
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Global variable to track MT5 connection status
mt5_connected = False

def initialize_mt5():
    """Initialize MetaTrader5 connection"""
    global mt5_connected
    try:
        if not mt5.initialize():
            logger.error("Failed to initialize MetaTrader5")
            return False
        
        # Test connection by getting account info
        account_info = mt5.account_info()
        if account_info is None:
            logger.error("Failed to get account info - MT5 might not be logged in")
            return False
        
        mt5_connected = True
        logger.info(f"✅ MetaTrader5 initialized successfully")
        logger.info(f"Account: {account_info.login}, Balance: {account_info.balance}")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing MetaTrader5: {e}")
        return False

def check_mt5_connection():
    """Check if MT5 is still connected"""
    global mt5_connected
    try:
        if not mt5_connected:
            return False
        
        # Quick connection test
        account_info = mt5.account_info()
        if account_info is None:
            mt5_connected = False
            return False
        
        return True
    except:
        mt5_connected = False
        return False

# Error handler decorator
def handle_errors(f):
    def wrapper(*args, **kwargs):
        try:
            if not check_mt5_connection():
                return jsonify({"error": "MetaTrader5 not connected"}), 500
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {e}")
            return jsonify({"error": str(e)}), 500
    wrapper.__name__ = f.__name__
    return wrapper

# Home page with simple interface
@app.route('/')
def home():
    """Simple web interface for testing"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MT5 Bridge Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; max-width: 800px; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .connected { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .disconnected { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .endpoint { background: #e9ecef; padding: 10px; margin: 5px 0; border-radius: 5px; }
            code { background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔌 MetaTrader5 Bridge Server</h1>
            <div class="status {{ 'connected' if mt5_connected else 'disconnected' }}">
                <strong>Status:</strong> {{ 'Connected to MT5 ✅' if mt5_connected else 'Not Connected ❌' }}
            </div>
            
            <h3>📡 Available Endpoints:</h3>
            <div class="endpoint"><code>GET /health</code> - Check server health</div>
            <div class="endpoint"><code>GET /account_info</code> - Get account information</div>
            <div class="endpoint"><code>POST /get_rates</code> - Get historical rates</div>
            <div class="endpoint"><code>POST /get_tick</code> - Get current price</div>
            
            <h3>🚀 Quick Test:</h3>
            <p><a href="/health" target="_blank">Test Health Check</a></p>
            <p><a href="/account_info" target="_blank">Test Account Info</a></p>
            
            <h3>📋 Setup Instructions:</h3>
            <ol>
                <li>Make sure MetaTrader5 terminal is running and logged in</li>
                <li>Start ngrok in another terminal: <code>ngrok http 5000</code></li>
                <li>Copy the ngrok URL and use it in your Colab notebook</li>
                <li>Test the connection using the endpoints above</li>
            </ol>
            
            <h3>⚠️ Security Notes:</h3>
            <ul>
                <li>Use demo accounts only for testing</li>
                <li>Don't share ngrok URLs publicly</li>
                <li>Monitor your MT5 account for any unexpected activity</li>
                <li>Stop this server when not in use</li>
            </ul>
        </div>
    </body>
    </html>
    """.replace('{{ mt5_connected }}', str(mt5_connected))
    
    return html

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = check_mt5_connection()
    return jsonify({
        "status": "healthy" if status else "unhealthy",
        "mt5_connected": status,
        "timestamp": datetime.now().isoformat(),
        "server": "MT5 Bridge Server v1.0"
    })

@app.route('/account_info', methods=['GET'])
@handle_errors
def get_account_info():
    """Get MT5 account information"""
    account_info = mt5.account_info()
    if account_info is None:
        return jsonify({"error": "Failed to get account info"}), 500
    
    return jsonify({
        "login": account_info.login,
        "balance": account_info.balance,
        "equity": account_info.equity,
        "margin": account_info.margin,
        "free_margin": account_info.margin_free,
        "margin_level": account_info.margin_level,
        "currency": account_info.currency,
        "leverage": account_info.leverage,
        "profit": account_info.profit,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/get_rates', methods=['POST'])
@handle_errors
def get_rates():
    """Get historical rates for a symbol"""
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    symbol = data.get('symbol', 'EURUSD')
    timeframe = data.get('timeframe', 'M1')
    count = data.get('count', 100)
    
    # Validate count
    if count > 10000:
        return jsonify({"error": "Count too large, maximum is 10000"}), 400
    
    # Map timeframe string to MT5 constant
    timeframe_map = {
        'M1': mt5.TIMEFRAME_M1,
        'M5': mt5.TIMEFRAME_M5,
        'M15': mt5.TIMEFRAME_M15,
        'M30': mt5.TIMEFRAME_M30,
        'H1': mt5.TIMEFRAME_H1,
        'H4': mt5.TIMEFRAME_H4,
        'D1': mt5.TIMEFRAME_D1,
        'W1': mt5.TIMEFRAME_W1,
        'MN1': mt5.TIMEFRAME_MN1
    }
    
    if timeframe not in timeframe_map:
        return jsonify({"error": f"Invalid timeframe: {timeframe}"}), 400
    
    mt5_timeframe = timeframe_map[timeframe]
    
    # Get rates
    rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return jsonify({"error": f"Failed to get rates for {symbol}"}), 500
    
    # Convert to DataFrame and then to JSON
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    return jsonify({
        "symbol": symbol,
        "timeframe": timeframe,
        "count": len(df),
        "data": df.to_dict('records'),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/get_tick', methods=['POST'])
@handle_errors
def get_tick():
    """Get current tick for a symbol"""
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    symbol = data.get('symbol', 'EURUSD')
    
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return jsonify({"error": f"Failed to get tick for {symbol}"}), 500
    
    return jsonify({
        "symbol": symbol,
        "time": datetime.fromtimestamp(tick.time).isoformat(),
        "bid": tick.bid,
        "ask": tick.ask,
        "last": tick.last,
        "volume": tick.volume,
        "flags": tick.flags,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/symbol_info', methods=['POST'])
@handle_errors
def get_symbol_info():
    """Get symbol information"""
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    symbol = data.get('symbol', 'EURUSD')
    
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return jsonify({"error": f"Symbol {symbol} not found"}), 500
    
    return jsonify({
        "symbol": symbol_info.name,
        "description": symbol_info.description,
        "currency_base": symbol_info.currency_base,
        "currency_profit": symbol_info.currency_profit,
        "currency_margin": symbol_info.currency_margin,
        "digits": symbol_info.digits,
        "point": symbol_info.point,
        "spread": symbol_info.spread,
        "volume_min": symbol_info.volume_min,
        "volume_max": symbol_info.volume_max,
        "volume_step": symbol_info.volume_step,
        "trade_mode": symbol_info.trade_mode,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/symbols', methods=['GET'])
@handle_errors
def get_symbols():
    """Get list of available symbols"""
    symbols = mt5.symbols_get()
    if symbols is None:
        return jsonify({"error": "Failed to get symbols"}), 500
    
    # Convert to simple list
    symbol_list = [symbol.name for symbol in symbols]
    
    return jsonify({
        "symbols": symbol_list,
        "count": len(symbol_list),
        "timestamp": datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

def main():
    """Main function"""
    print("🚀 Starting MetaTrader5 Bridge Server...")
    print("=" * 50)
    
    # Check if MT5 is available
    if not initialize_mt5():
        print("❌ Failed to initialize MetaTrader5!")
        print("Please ensure:")
        print("1. MetaTrader5 terminal is running")
        print("2. You are logged into an account")
        print("3. MetaTrader5 Python package is installed")
        sys.exit(1)
    
    print(f"✅ Server starting on http://localhost:5000")
    print(f"📊 MT5 Connection: {'Connected' if mt5_connected else 'Disconnected'}")
    print("=" * 50)
    print("📋 Next steps:")
    print("1. Open another terminal")
    print("2. Run: ngrok http 5000")
    print("3. Copy the ngrok URL (https://xxxxx.ngrok.io)")
    print("4. Use that URL in your Colab notebook")
    print("=" * 50)
    print("🌐 Web interface: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start Flask server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Set to True for development
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
    finally:
        # Cleanup MT5 connection
        if mt5_connected:
            mt5.shutdown()
            print("🔒 MetaTrader5 connection closed")

if __name__ == '__main__':
    main()