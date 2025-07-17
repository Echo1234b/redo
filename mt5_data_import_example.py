#!/usr/bin/env python3
"""
MetaTrader 5 Data Import Example
Simple demonstration of how to import data from MT5 platform
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time

def connect_to_mt5(login=None, password=None, server=None):
    """
    Connect to MetaTrader 5
    
    Args:
        login: MT5 account login (optional)
        password: MT5 account password (optional)
        server: MT5 server name (optional)
    
    Returns:
        bool: True if connected successfully
    """
    print("🔗 Connecting to MetaTrader 5...")
    
    # Initialize MT5
    if not mt5.initialize():
        print("❌ Failed to initialize MetaTrader 5")
        return False
    
    # Login if credentials provided
    if login and password and server:
        if not mt5.login(login, password, server):
            print(f"❌ Login failed: {mt5.last_error()}")
            return False
        print(f"✅ Logged in to account: {login}")
    
    # Get account info
    account_info = mt5.account_info()
    if account_info is None:
        print("❌ Failed to get account info")
        return False
    
    print(f"✅ Connected to MT5")
    print(f"   Account: {account_info.login}")
    print(f"   Server: {account_info.server}")
    print(f"   Balance: {account_info.balance} {account_info.currency}")
    
    return True

def get_available_symbols(search_term="BTC"):
    """
    Get available symbols matching search term
    
    Args:
        search_term: Symbol search pattern
    
    Returns:
        list: List of matching symbols
    """
    print(f"🔍 Searching for symbols containing '{search_term}'...")
    
    # Get all symbols
    symbols = mt5.symbols_get()
    if symbols is None:
        print("❌ Failed to get symbols")
        return []
    
    # Filter symbols
    matching_symbols = [
        symbol.name for symbol in symbols 
        if search_term.upper() in symbol.name.upper()
    ]
    
    print(f"✅ Found {len(matching_symbols)} matching symbols:")
    for symbol in matching_symbols[:10]:  # Show first 10
        print(f"   - {symbol}")
    
    return matching_symbols

def get_current_price(symbol):
    """
    Get current price for a symbol
    
    Args:
        symbol: Trading symbol
    
    Returns:
        dict: Current price information
    """
    print(f"📊 Getting current price for {symbol}...")
    
    # Get current tick
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Failed to get price for {symbol}")
        return {}
    
    price_info = {
        'symbol': symbol,
        'bid': tick.bid,
        'ask': tick.ask,
        'last': tick.last,
        'volume': tick.volume,
        'time': datetime.fromtimestamp(tick.time),
        'spread': tick.ask - tick.bid
    }
    
    print(f"✅ Current price for {symbol}:")
    print(f"   Bid: {price_info['bid']:.5f}")
    print(f"   Ask: {price_info['ask']:.5f}")
    print(f"   Last: {price_info['last']:.5f}")
    print(f"   Spread: {price_info['spread']:.5f}")
    print(f"   Time: {price_info['time']}")
    
    return price_info

def get_historical_data(symbol, timeframe="H1", count=100):
    """
    Get historical OHLCV data
    
    Args:
        symbol: Trading symbol
        timeframe: Timeframe (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
        count: Number of bars to retrieve
    
    Returns:
        pd.DataFrame: Historical data
    """
    print(f"📈 Getting historical data for {symbol} ({timeframe}, {count} bars)...")
    
    # Map timeframe strings to MT5 constants
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
        print(f"❌ Invalid timeframe: {timeframe}")
        return pd.DataFrame()
    
    mt5_timeframe = timeframe_map[timeframe]
    
    # Get historical data
    rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
    if rates is None:
        print(f"❌ Failed to get historical data for {symbol}")
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    
    # Rename columns
    df.columns = ['Open', 'High', 'Low', 'Close', 'tick_volume', 'spread', 'real_volume']
    df = df[['Open', 'High', 'Low', 'Close', 'tick_volume']].copy()
    df.rename(columns={'tick_volume': 'Volume'}, inplace=True)
    
    print(f"✅ Retrieved {len(df)} bars of historical data")
    print(f"   Date range: {df.index[0]} to {df.index[-1]}")
    print(f"   Latest close: {df['Close'].iloc[-1]:.5f}")
    
    return df

def get_account_summary():
    """
    Get account summary information
    
    Returns:
        dict: Account information
    """
    print("💼 Getting account summary...")
    
    # Get account info
    account_info = mt5.account_info()
    if account_info is None:
        print("❌ Failed to get account info")
        return {}
    
    account_data = {
        'login': account_info.login,
        'server': account_info.server,
        'balance': account_info.balance,
        'equity': account_info.equity,
        'margin': account_info.margin,
        'free_margin': account_info.margin_free,
        'margin_level': account_info.margin_level,
        'currency': account_info.currency,
        'leverage': account_info.leverage
    }
    
    print("✅ Account Summary:")
    print(f"   Login: {account_data['login']}")
    print(f"   Server: {account_data['server']}")
    print(f"   Balance: {account_data['balance']:.2f} {account_data['currency']}")
    print(f"   Equity: {account_data['equity']:.2f} {account_data['currency']}")
    print(f"   Free Margin: {account_data['free_margin']:.2f} {account_data['currency']}")
    print(f"   Leverage: 1:{account_data['leverage']}")
    
    return account_data

def get_positions():
    """
    Get open positions
    
    Returns:
        pd.DataFrame: Open positions
    """
    print("📈 Getting open positions...")
    
    positions = mt5.positions_get()
    if positions is None or len(positions) == 0:
        print("✅ No open positions")
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    print(f"✅ Found {len(df)} open positions:")
    for _, pos in df.iterrows():
        print(f"   {pos['symbol']}: {pos['type']} {pos['volume']} @ {pos['price_open']:.5f}")
    
    return df

def disconnect_mt5():
    """
    Disconnect from MetaTrader 5
    """
    print("🔌 Disconnecting from MetaTrader 5...")
    mt5.shutdown()
    print("✅ Disconnected successfully")

def main():
    """
    Main function demonstrating MT5 data import
    """
    print("🚀 MetaTrader 5 Data Import Example")
    print("=" * 50)
    
    try:
        # Step 1: Connect to MT5
        # For demo/testing, you can connect without credentials if MT5 is already logged in
        if not connect_to_mt5():
            print("❌ Failed to connect to MT5. Make sure MT5 terminal is running and logged in.")
            return
        
        # Step 2: Get available symbols
        btc_symbols = get_available_symbols("BTC")
        if not btc_symbols:
            print("❌ No Bitcoin symbols found. Try different search terms.")
            return
        
        # Use first Bitcoin symbol found
        symbol = btc_symbols[0]
        print(f"\n🎯 Using symbol: {symbol}")
        
        # Step 3: Get current price
        current_price = get_current_price(symbol)
        if not current_price:
            print(f"❌ Failed to get current price for {symbol}")
            return
        
        # Step 4: Get historical data
        print(f"\n📊 Importing historical data...")
        df = get_historical_data(symbol, "H1", 100)
        if df.empty:
            print(f"❌ Failed to get historical data for {symbol}")
            return
        
        # Display sample data
        print("\n📋 Sample Historical Data:")
        print(df.tail().to_string())
        
        # Step 5: Get account information
        print(f"\n💼 Account Information:")
        account_info = get_account_summary()
        
        # Step 6: Get positions
        print(f"\n📈 Trading Positions:")
        positions = get_positions()
        
        # Step 7: Demonstrate real-time updates
        print(f"\n🔄 Real-time Price Updates (5 updates):")
        for i in range(5):
            price = get_current_price(symbol)
            if price:
                print(f"   Update {i+1}: {price['last']:.5f} at {price['time']}")
            time.sleep(2)  # Wait 2 seconds between updates
        
        print(f"\n✅ Data import example completed successfully!")
        print(f"📊 Retrieved {len(df)} historical bars for {symbol}")
        print(f"💰 Current price: {current_price['last']:.5f}")
        print(f"💼 Account balance: {account_info['balance']:.2f} {account_info['currency']}")
        
    except Exception as e:
        print(f"❌ Error during data import: {str(e)}")
    
    finally:
        # Always disconnect
        disconnect_mt5()

if __name__ == "__main__":
    main()