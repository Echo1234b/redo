#!/usr/bin/env python3
"""
MetaTrader 5 Integration Module for Bitcoin Live Analyzer
Imports real-time and historical data from MetaTrader 5 platform
Windows-optimized version with robust error handling
"""

import sys
import os
import platform
import logging
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import MetaTrader5 with robust error handling
MT5_AVAILABLE = False
mt5 = None

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
    logger.info("✅ MetaTrader5 package imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ MetaTrader5 not available: {str(e)}")
    logger.info("App will run in demo mode without live MT5 data")
except Exception as e:
    logger.error(f"❌ Unexpected error importing MetaTrader5: {str(e)}")

# Windows-specific MT5 path detection
def detect_mt5_installation():
    """Detect MetaTrader 5 installation on Windows"""
    if platform.system() != "Windows":
        return None
    
    import winreg
    possible_paths = [
        r"C:\Program Files\MetaTrader 5\terminal64.exe",
        r"C:\Program Files (x86)\MetaTrader 5\terminal.exe",
        r"C:\Users\{}\AppData\Roaming\MetaQuotes\Terminal".format(sys.platform.get('USERNAME', ''))
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Check registry
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\MetaQuotes\Terminal") as key:
            path = winreg.QueryValueEx(key, "Path")[0]
            return path
    except:
        pass
    
    return None

class MetaTraderDataProvider:
    """
    MetaTrader 5 data provider for Bitcoin and other trading instruments
    Windows-optimized with comprehensive error handling
    """
    
    def __init__(self):
        self.mt5_connected = False
        self.available_symbols = []
        self.account_info = None
        self.demo_mode = not MT5_AVAILABLE
        
        if not MT5_AVAILABLE:
            logger.info("🔄 Running in DEMO MODE - No MT5 connection available")
            self._setup_demo_data()
        
    def _setup_demo_data(self):
        """Setup demo data when MT5 is not available"""
        self.available_symbols = ['BTCUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'XAUUSD']
        logger.info("📊 Demo symbols loaded: " + ", ".join(self.available_symbols))
        
    def initialize_mt5(self, login: int = None, password: str = None, server: str = None, path: str = None):
        """
        Initialize MetaTrader 5 connection with Windows optimizations
        
        Args:
            login: MT5 account login (optional if already logged in)
            password: MT5 account password (optional if already logged in)
            server: MT5 server name (optional if already logged in)
            path: Custom MT5 installation path (Windows only)
        """
        if not MT5_AVAILABLE:
            logger.warning("⚠️ MT5 not available - staying in demo mode")
            return False
            
        try:
            # Windows-specific initialization
            if platform.system() == "Windows":
                if path:
                    # Initialize with custom path
                    if not mt5.initialize(path=path):
                        logger.error(f"Failed to initialize MT5 with path: {path}")
                        return False
                else:
                    # Auto-detect MT5 installation
                    detected_path = detect_mt5_installation()
                    if detected_path:
                        logger.info(f"🔍 Detected MT5 installation: {detected_path}")
                        if not mt5.initialize(path=detected_path):
                            logger.error("Failed to initialize MT5 with detected path")
                            # Try default initialization
                            if not mt5.initialize():
                                logger.error("Failed to initialize MT5 (default)")
                                return False
                    else:
                        # Try default initialization
                        if not mt5.initialize():
                            logger.error("Failed to initialize MT5 (no path detected)")
                            return False
            else:
                # Non-Windows initialization
                if not mt5.initialize():
                    logger.error("Failed to initialize MetaTrader 5")
                    return False
            
            # Check if MT5 terminal is running
            terminal_info = mt5.terminal_info()
            if terminal_info is None:
                logger.error("MT5 terminal is not running or not accessible")
                return False
                
            logger.info(f"✅ MT5 Terminal connected: {terminal_info.name}")
            
            # Login if credentials provided
            if login and password and server:
                if not mt5.login(login, password, server):
                    error_code = mt5.last_error()
                    logger.error(f"Failed to login to MT5: {error_code}")
                    return False
                logger.info(f"✅ Logged in to server: {server}")
            
            # Get account info
            self.account_info = mt5.account_info()
            if self.account_info is None:
                logger.warning("⚠️ No account info available (demo account or not logged in)")
                # Continue without account info for demo accounts
            else:
                logger.info(f"✅ Account connected: {self.account_info.login}")
            
            # Get available symbols
            symbols = mt5.symbols_get()
            if symbols is None:
                logger.error("Failed to get symbols")
                return False
            
            self.available_symbols = [symbol.name for symbol in symbols if symbol.name]
            self.mt5_connected = True
            self.demo_mode = False
            
            logger.info(f"✅ Successfully connected to MT5")
            logger.info(f"📊 Available symbols: {len(self.available_symbols)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing MT5: {str(e)}")
            # Check if it's a common Windows issue
            if platform.system() == "Windows":
                logger.info("💡 Windows troubleshooting tips:")
                logger.info("   1. Make sure MT5 terminal is running")
                logger.info("   2. Run as administrator if needed")
                logger.info("   3. Check Windows Defender/antivirus settings")
                logger.info("   4. Verify MT5 allows DLL imports")
            return False
    
    def get_symbol_info(self, symbol: str) -> Dict:
        """
        Get symbol information with demo fallback
        """
        if self.demo_mode:
            return self._get_demo_symbol_info(symbol)
            
        if not self.mt5_connected:
            return {}
        
        try:
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"Symbol {symbol} not found")
                return {}
            
            return {
                'name': symbol_info.name,
                'description': symbol_info.description,
                'currency_base': symbol_info.currency_base,
                'currency_profit': symbol_info.currency_profit,
                'digits': symbol_info.digits,
                'point': symbol_info.point,
                'trade_mode': symbol_info.trade_mode,
                'min_lot': symbol_info.volume_min,
                'max_lot': symbol_info.volume_max,
                'lot_step': symbol_info.volume_step,
                'spread': symbol_info.spread
            }
            
        except Exception as e:
            logger.error(f"Error getting symbol info for {symbol}: {str(e)}")
            return {}
    
    def _get_demo_symbol_info(self, symbol: str) -> Dict:
        """Demo symbol info for when MT5 is not available"""
        demo_symbols = {
            'BTCUSD': {
                'name': 'BTCUSD',
                'description': 'Bitcoin vs US Dollar',
                'currency_base': 'BTC',
                'currency_profit': 'USD',
                'digits': 2,
                'point': 0.01,
                'trade_mode': 4,
                'min_lot': 0.01,
                'max_lot': 100.0,
                'lot_step': 0.01,
                'spread': 50
            },
            'EURUSD': {
                'name': 'EURUSD',
                'description': 'Euro vs US Dollar',
                'currency_base': 'EUR',
                'currency_profit': 'USD',
                'digits': 5,
                'point': 0.00001,
                'trade_mode': 4,
                'min_lot': 0.01,
                'max_lot': 100.0,
                'lot_step': 0.01,
                'spread': 3
            }
        }
        return demo_symbols.get(symbol, {})
    
    def get_historical_data(self, symbol: str, timeframe: str, count: int = 1000) -> pd.DataFrame:
        """
        Get historical data with demo fallback
        """
        if self.demo_mode:
            return self._get_demo_historical_data(symbol, timeframe, count)
            
        if not self.mt5_connected:
            logger.error("MT5 not connected")
            return pd.DataFrame()
        
        try:
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
            
            mt5_timeframe = timeframe_map.get(timeframe, mt5.TIMEFRAME_H1)
            
            # Get historical data
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
            
            if rates is None or len(rates) == 0:
                logger.error(f"No data received for {symbol}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            # Rename columns to standard format
            df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'tick_volume': 'Volume'
            }, inplace=True)
            
            logger.info(f"✅ Retrieved {len(df)} records for {symbol} ({timeframe})")
            return df
            
        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            return pd.DataFrame()
    
    def _get_demo_historical_data(self, symbol: str, timeframe: str, count: int = 1000) -> pd.DataFrame:
        """Generate demo historical data when MT5 is not available"""
        logger.info(f"📊 Generating demo data for {symbol} ({count} points)")
        
        # Generate realistic price data
        np.random.seed(42)  # For reproducible demo data
        
        # Starting prices for different symbols
        start_prices = {
            'BTCUSD': 45000.0,
            'EURUSD': 1.0850,
            'GBPUSD': 1.2650,
            'USDJPY': 149.50,
            'XAUUSD': 2050.0
        }
        
        start_price = start_prices.get(symbol, 1.0000)
        
        # Generate time series
        end_time = datetime.now()
        time_deltas = {
            'M1': timedelta(minutes=1),
            'M5': timedelta(minutes=5),
            'M15': timedelta(minutes=15),
            'M30': timedelta(minutes=30),
            'H1': timedelta(hours=1),
            'H4': timedelta(hours=4),
            'D1': timedelta(days=1),
            'W1': timedelta(weeks=1),
            'MN1': timedelta(days=30)
        }
        
        delta = time_deltas.get(timeframe, timedelta(hours=1))
        times = [end_time - delta * i for i in range(count)]
        times.reverse()
        
        # Generate price movements (random walk with trend)
        prices = []
        current_price = start_price
        
        for i in range(count):
            # Add some trend and volatility
            trend = 0.0001 if symbol == 'BTCUSD' else 0.00001
            volatility = 0.02 if symbol == 'BTCUSD' else 0.001
            
            change = np.random.normal(trend, volatility)
            current_price *= (1 + change)
            prices.append(current_price)
        
        # Create OHLCV data
        data = []
        for i, (time, price) in enumerate(zip(times, prices)):
            # Generate realistic OHLC from price
            volatility = price * 0.001  # 0.1% volatility
            high = price + np.random.uniform(0, volatility)
            low = price - np.random.uniform(0, volatility)
            open_price = prices[i-1] if i > 0 else price
            close_price = price
            volume = np.random.randint(100, 1000)
            
            data.append({
                'time': time,
                'Open': open_price,
                'High': max(open_price, high, close_price),
                'Low': min(open_price, low, close_price),
                'Close': close_price,
                'Volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('time', inplace=True)
        
        return df
    
    def get_current_price(self, symbol: str) -> Dict:
        """
        Get current price with demo fallback
        """
        if self.demo_mode:
            return self._get_demo_current_price(symbol)
            
        if not self.mt5_connected:
            return {}
        
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"No current price for {symbol}")
                return {}
            
            return {
                'symbol': symbol,
                'bid': tick.bid,
                'ask': tick.ask,
                'price': (tick.bid + tick.ask) / 2,
                'spread': tick.ask - tick.bid,
                'time': datetime.fromtimestamp(tick.time)
            }
            
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {str(e)}")
            return {}
    
    def _get_demo_current_price(self, symbol: str) -> Dict:
        """Demo current price when MT5 is not available"""
        demo_prices = {
            'BTCUSD': {'bid': 44980.50, 'ask': 45019.50},
            'EURUSD': {'bid': 1.08495, 'ask': 1.08505},
            'GBPUSD': {'bid': 1.26485, 'ask': 1.26495},
            'USDJPY': {'bid': 149.485, 'ask': 149.495},
            'XAUUSD': {'bid': 2049.50, 'ask': 2050.50}
        }
        
        if symbol in demo_prices:
            price_data = demo_prices[symbol]
            return {
                'symbol': symbol,
                'bid': price_data['bid'],
                'ask': price_data['ask'],
                'price': (price_data['bid'] + price_data['ask']) / 2,
                'spread': price_data['ask'] - price_data['bid'],
                'time': datetime.now()
            }
        return {}
    
    def shutdown(self):
        """
        Properly shutdown MT5 connection
        """
        if MT5_AVAILABLE and self.mt5_connected:
            try:
                mt5.shutdown()
                self.mt5_connected = False
                logger.info("✅ MT5 connection closed properly")
            except Exception as e:
                logger.error(f"Error shutting down MT5: {str(e)}")

# Import streamlit only when needed to avoid dependency issues
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    logger.warning("Streamlit not available for UI components")

class MetaTraderStreamlitUI:
    """
    Streamlit UI components for MetaTrader integration
    """
    
    @staticmethod
    def render_connection_form() -> Optional[Tuple[int, str, str]]:
        """Render MT5 connection form"""
        if not STREAMLIT_AVAILABLE:
            return None
            
        st.sidebar.header("🔌 MetaTrader 5 Connection")
        
        if not MT5_AVAILABLE:
            st.sidebar.warning("⚠️ MT5 Package Not Available")
            st.sidebar.info("Running in Demo Mode")
            return None
        
        # Connection status
        if 'mt5_provider' in st.session_state and st.session_state.mt5_provider.mt5_connected:
            st.sidebar.success("✅ Connected to MT5")
            if st.sidebar.button("🔌 Disconnect"):
                st.session_state.mt5_provider.shutdown()
                st.experimental_rerun()
            return None
        
        # Connection form
        with st.sidebar.form("mt5_connection"):
            st.write("Enter your MT5 credentials:")
            
            login = st.number_input("Login", min_value=1, value=None, format="%d")
            password = st.text_input("Password", type="password")
            server = st.selectbox("Server", [
                "Demo Server",
                "MetaQuotes-Demo",
                "Custom"
            ])
            
            if server == "Custom":
                server = st.text_input("Custom Server")
            
            # Windows-specific options
            if platform.system() == "Windows":
                st.write("Windows Options:")
                custom_path = st.text_input("MT5 Path (optional)", 
                                          placeholder="C:\\Program Files\\MetaTrader 5\\terminal64.exe")
            else:
                custom_path = None
            
            submit = st.form_submit_button("🔗 Connect")
            
            if submit and login and password and server:
                return (int(login), password, server)
        
        return None
    
    @staticmethod
    def render_symbol_selector(mt5_provider: MetaTraderDataProvider) -> Optional[str]:
        """Render symbol selection dropdown"""
        if not STREAMLIT_AVAILABLE:
            return None
            
        st.sidebar.header("📊 Symbol Selection")
        
        if mt5_provider.demo_mode:
            st.sidebar.info("🎮 Demo Mode Active")
        
        symbols = mt5_provider.available_symbols
        if not symbols:
            st.sidebar.warning("No symbols available")
            return None
        
        # Filter for common trading symbols
        common_symbols = [s for s in symbols if any(x in s for x in ['BTC', 'EUR', 'GBP', 'USD', 'XAU'])]
        if common_symbols:
            symbols = common_symbols
        
        selected = st.sidebar.selectbox(
            "Choose Symbol:",
            options=symbols,
            index=0 if 'BTCUSD' not in symbols else symbols.index('BTCUSD')
        )
        
        return selected
    
    @staticmethod
    def render_timeframe_selector() -> str:
        """Render timeframe selection"""
        if not STREAMLIT_AVAILABLE:
            return "H1"
            
        timeframes = {
            "1 Minute": "M1",
            "5 Minutes": "M5", 
            "15 Minutes": "M15",
            "30 Minutes": "M30",
            "1 Hour": "H1",
            "4 Hours": "H4",
            "Daily": "D1",
            "Weekly": "W1",
            "Monthly": "MN1"
        }
        
        selected = st.sidebar.selectbox(
            "Timeframe:",
            options=list(timeframes.keys()),
            index=4  # Default to 1 Hour
        )
        
        return timeframes[selected]
    
    @staticmethod
    def render_account_info(mt5_provider: MetaTraderDataProvider):
        """Render account information"""
        if not STREAMLIT_AVAILABLE:
            return
            
        if mt5_provider.demo_mode:
            st.sidebar.info("🎮 Demo Account")
            return
            
        if not mt5_provider.account_info:
            return
        
        account = mt5_provider.account_info
        st.sidebar.header("💼 Account Info")
        st.sidebar.write(f"**Login:** {account.login}")
        st.sidebar.write(f"**Server:** {account.server}")
        st.sidebar.write(f"**Balance:** {account.balance} {account.currency}")
        st.sidebar.write(f"**Equity:** {account.equity} {account.currency}")
        st.sidebar.write(f"**Leverage:** 1:{account.leverage}")
    
    @staticmethod
    def render_connection_status(mt5_provider: MetaTraderDataProvider):
        """Render connection status"""
        if not STREAMLIT_AVAILABLE:
            return
            
        if mt5_provider.demo_mode:
            st.sidebar.success("🎮 Demo Mode - Simulated Data")
        elif mt5_provider.mt5_connected:
            st.sidebar.success("✅ MT5 Connected")
        else:
            st.sidebar.error("❌ MT5 Disconnected")

def test_mt5_connection():
    """Test MT5 connection functionality"""
    print("🧪 Testing MetaTrader 5 Connection...")
    print("=" * 50)
    
    # Initialize provider
    provider = MetaTraderDataProvider()
    
    if provider.demo_mode:
        print("🎮 Running in DEMO mode")
        
        # Test demo data
        symbols = provider.available_symbols
        print(f"📊 Available symbols: {symbols}")
        
        # Test demo historical data
        if symbols:
            symbol = symbols[0]
            df = provider.get_historical_data(symbol, "H1", 100)
            print(f"📈 Demo data for {symbol}: {len(df)} records")
            
            # Test demo current price
            price = provider.get_current_price(symbol)
            if price:
                print(f"💰 Demo price: {price['price']}")
        
    else:
        # Try to connect to MT5
        if provider.initialize_mt5():
            print("✅ MT5 connection successful!")
            
            # Test symbols
            symbols = provider.available_symbols[:5]  # First 5 symbols
            print(f"📊 Available symbols (first 5): {symbols}")
            
            # Test data retrieval
            if symbols:
                symbol = symbols[0]
                df = provider.get_historical_data(symbol, "H1", 10)
                print(f"📈 Historical data for {symbol}: {len(df)} records")
                
                # Test current price
                price = provider.get_current_price(symbol)
                if price:
                    print(f"💰 Current price: {price['price']}")
            
            # Cleanup
            provider.shutdown()
            
        else:
            print("❌ Failed to initialize MT5")
            print("💡 Will run in demo mode")

if __name__ == "__main__":
    test_mt5_connection()