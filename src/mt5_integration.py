#!/usr/bin/env python3
"""
MetaTrader 5 Integration Module for Bitcoin Live Analyzer
Imports real-time and historical data from MetaTrader 5 platform
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Tuple, Optional
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetaTraderDataProvider:
    """
    MetaTrader 5 data provider for Bitcoin and other trading instruments
    """
    
    def __init__(self):
        self.mt5_connected = False
        self.available_symbols = []
        self.account_info = None
        
    def initialize_mt5(self, login: int = None, password: str = None, server: str = None):
        """
        Initialize MetaTrader 5 connection
        
        Args:
            login: MT5 account login (optional if already logged in)
            password: MT5 account password (optional if already logged in)
            server: MT5 server name (optional if already logged in)
        """
        try:
            # Initialize MT5
            if not mt5.initialize():
                logger.error("Failed to initialize MetaTrader 5")
                return False
            
            # Login if credentials provided
            if login and password and server:
                if not mt5.login(login, password, server):
                    logger.error(f"Failed to login to MT5: {mt5.last_error()}")
                    return False
            
            # Get account info
            self.account_info = mt5.account_info()
            if self.account_info is None:
                logger.error("Failed to get account info")
                return False
            
            # Get available symbols
            symbols = mt5.symbols_get()
            if symbols is None:
                logger.error("Failed to get symbols")
                return False
            
            self.available_symbols = [symbol.name for symbol in symbols]
            self.mt5_connected = True
            
            logger.info(f"Successfully connected to MT5. Account: {self.account_info.login}")
            logger.info(f"Available symbols: {len(self.available_symbols)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing MT5: {str(e)}")
            return False
    
    def get_symbol_info(self, symbol: str) -> Dict:
        """
        Get symbol information
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSD', 'EURUSD')
            
        Returns:
            Dictionary with symbol information
        """
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
                'volume_min': symbol_info.volume_min,
                'volume_max': symbol_info.volume_max,
                'volume_step': symbol_info.volume_step,
                'margin_required': symbol_info.margin_required
            }
            
        except Exception as e:
            logger.error(f"Error getting symbol info for {symbol}: {str(e)}")
            return {}
    
    def get_historical_data(self, symbol: str, timeframe: str, count: int = 1000, start_date: datetime = None) -> pd.DataFrame:
        """
        Get historical price data from MetaTrader 5
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSD')
            timeframe: MT5 timeframe (e.g., 'M1', 'M5', 'H1', 'D1')
            count: Number of bars to retrieve
            start_date: Start date for data retrieval (optional)
            
        Returns:
            DataFrame with OHLCV data
        """
        if not self.mt5_connected:
            logger.error("MT5 not connected")
            return pd.DataFrame()
        
        try:
            # Convert timeframe string to MT5 constant
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
            
            mt5_timeframe = timeframe_map.get(timeframe)
            if mt5_timeframe is None:
                logger.error(f"Unsupported timeframe: {timeframe}")
                return pd.DataFrame()
            
            # Get rates
            if start_date:
                rates = mt5.copy_rates_from(symbol, mt5_timeframe, start_date, count)
            else:
                rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
            
            if rates is None or len(rates) == 0:
                logger.error(f"No data received for {symbol} {timeframe}")
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
            
            # Remove unnecessary columns
            if 'spread' in df.columns:
                df.drop('spread', axis=1, inplace=True)
            if 'real_volume' in df.columns:
                df.drop('real_volume', axis=1, inplace=True)
            
            logger.info(f"Retrieved {len(df)} bars for {symbol} {timeframe}")
            return df
            
        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            return pd.DataFrame()
    
    def get_current_price(self, symbol: str) -> Dict:
        """
        Get current price information for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dictionary with current price info
        """
        if not self.mt5_connected:
            return {}
        
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"Failed to get tick data for {symbol}")
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
    
    def get_positions(self) -> pd.DataFrame:
        """Get open positions"""
        if not self.mt5_connected:
            return pd.DataFrame()
        
        try:
            positions = mt5.positions_get()
            if positions is None:
                return pd.DataFrame()
            
            df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys()) if positions else pd.DataFrame()
            return df
            
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return pd.DataFrame()
    
    def get_orders(self) -> pd.DataFrame:
        """Get pending orders"""
        if not self.mt5_connected:
            return pd.DataFrame()
        
        try:
            orders = mt5.orders_get()
            if orders is None:
                return pd.DataFrame()
            
            df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys()) if orders else pd.DataFrame()
            return df
            
        except Exception as e:
            logger.error(f"Error getting orders: {str(e)}")
            return pd.DataFrame()
    
    def get_deals_history(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get historical deals"""
        if not self.mt5_connected:
            return pd.DataFrame()
        
        try:
            deals = mt5.history_deals_get(start_date, end_date)
            if deals is None:
                return pd.DataFrame()
            
            df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys()) if deals else pd.DataFrame()
            return df
            
        except Exception as e:
            logger.error(f"Error getting deals history: {str(e)}")
            return pd.DataFrame()
    
    def shutdown(self):
        """Shutdown MT5 connection"""
        if self.mt5_connected:
            mt5.shutdown()
            self.mt5_connected = False
            logger.info("MT5 connection closed")


class MetaTraderStreamlitUI:
    """
    Streamlit UI components for MetaTrader integration
    """
    
    @staticmethod
    def render_connection_form() -> Optional[Tuple[int, str, str]]:
        """
        Render MT5 connection form in sidebar
        
        Returns:
            Tuple of (login, password, server) if submitted, None otherwise
        """
        st.sidebar.markdown("## 🔌 MT5 Connection")
        
        with st.sidebar.form("mt5_connection"):
            login = st.number_input("Login", min_value=1, step=1, value=None)
            password = st.text_input("Password", type="password")
            server = st.text_input("Server", placeholder="e.g., MetaQuotes-Demo")
            
            submitted = st.form_submit_button("Connect to MT5")
            
            if submitted and login and password and server:
                return int(login), password, server
        
        return None
    
    @staticmethod
    def render_symbol_selector(mt5_provider: MetaTraderDataProvider) -> Optional[str]:
        """
        Render symbol selection interface
        
        Args:
            mt5_provider: MetaTrader data provider instance
            
        Returns:
            Selected symbol or None
        """
        st.sidebar.markdown("## 📊 Symbol Selection")
        
        if not mt5_provider.mt5_connected:
            st.sidebar.warning("Connect to MT5 first")
            return None
        
        # Common crypto symbols to prioritize
        crypto_symbols = ['BTCUSD', 'ETHUSD', 'LTCUSD', 'BCHUSD', 'XRPUSD', 'ADAUSD', 'DOTUSD']
        
        # Filter available symbols to show crypto first
        available_crypto = [s for s in crypto_symbols if s in mt5_provider.available_symbols]
        other_symbols = [s for s in mt5_provider.available_symbols if s not in crypto_symbols]
        
        # Combine lists
        symbol_options = available_crypto + other_symbols[:50]  # Limit to 50 other symbols
        
        if not symbol_options:
            st.sidebar.error("No symbols available")
            return None
        
        selected_symbol = st.sidebar.selectbox(
            "Select Trading Symbol",
            options=symbol_options,
            index=0 if available_crypto else 0
        )
        
        # Show symbol info
        if selected_symbol:
            symbol_info = mt5_provider.get_symbol_info(selected_symbol)
            if symbol_info:
                st.sidebar.info(f"**{symbol_info['description']}**\n"
                              f"Base: {symbol_info['currency_base']}\n"
                              f"Profit: {symbol_info['currency_profit']}\n"
                              f"Digits: {symbol_info['digits']}")
        
        return selected_symbol
    
    @staticmethod
    def render_timeframe_selector() -> str:
        """
        Render timeframe selection interface
        
        Returns:
            Selected timeframe
        """
        st.sidebar.markdown("## ⏰ Timeframe")
        
        timeframes = {
            'M1': '1 Minute',
            'M5': '5 Minutes',
            'M15': '15 Minutes',
            'M30': '30 Minutes',
            'H1': '1 Hour',
            'H4': '4 Hours',
            'D1': '1 Day',
            'W1': '1 Week',
            'MN1': '1 Month'
        }
        
        selected_tf = st.sidebar.selectbox(
            "Select Timeframe",
            options=list(timeframes.keys()),
            format_func=lambda x: timeframes[x],
            index=4  # Default to H1
        )
        
        return selected_tf
    
    @staticmethod
    def render_account_info(mt5_provider: MetaTraderDataProvider):
        """
        Render account information
        
        Args:
            mt5_provider: MetaTrader data provider instance
        """
        if not mt5_provider.mt5_connected or not mt5_provider.account_info:
            return
        
        st.sidebar.markdown("## 💼 Account Info")
        
        account = mt5_provider.account_info
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Balance", f"${account.balance:,.2f}")
            st.metric("Equity", f"${account.equity:,.2f}")
        
        with col2:
            st.metric("Margin", f"${account.margin:,.2f}")
            st.metric("Free Margin", f"${account.margin_free:,.2f}")
        
        # Profit/Loss
        profit = account.profit
        profit_color = "normal" if profit >= 0 else "inverse"
        st.sidebar.metric("Profit/Loss", f"${profit:,.2f}", delta=profit, delta_color=profit_color)
        
        # Additional info
        st.sidebar.text(f"Server: {account.server}")
        st.sidebar.text(f"Company: {account.company}")
        st.sidebar.text(f"Currency: {account.currency}")
    
    @staticmethod
    def render_connection_status(mt5_provider: MetaTraderDataProvider):
        """
        Render connection status indicator
        
        Args:
            mt5_provider: MetaTrader data provider instance
        """
        if mt5_provider.mt5_connected:
            st.sidebar.success("🟢 MT5 Connected")
        else:
            st.sidebar.error("🔴 MT5 Disconnected")


# Example usage and testing functions
def test_mt5_connection():
    """Test MT5 connection functionality"""
    provider = MetaTraderDataProvider()
    
    # Test initialization
    if provider.initialize_mt5():
        print("✅ MT5 initialized successfully")
        
        # Test symbol info
        symbol_info = provider.get_symbol_info("BTCUSD")
        if symbol_info:
            print(f"✅ Symbol info retrieved: {symbol_info['description']}")
        
        # Test historical data
        df = provider.get_historical_data("BTCUSD", "H1", 100)
        if not df.empty:
            print(f"✅ Historical data retrieved: {len(df)} bars")
            print(df.tail())
        
        # Test current price
        price = provider.get_current_price("BTCUSD")
        if price:
            print(f"✅ Current price: {price['price']}")
        
        # Cleanup
        provider.shutdown()
        
    else:
        print("❌ Failed to initialize MT5")


if __name__ == "__main__":
    test_mt5_connection()