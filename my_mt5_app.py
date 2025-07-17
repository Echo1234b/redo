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
