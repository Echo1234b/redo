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
