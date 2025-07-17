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
                'spread': symbol_info.spread,
                'volume_min': symbol_info.volume_min,
                'volume_max': symbol_info.volume_max,
                'trade_tick_value': symbol_info.trade_tick_value,
                'trade_tick_size': symbol_info.trade_tick_size,
            }
            
        except Exception as e:
            logger.error(f"Error getting symbol info: {str(e)}")
            return {}
    
    def get_current_price(self, symbol: str) -> Dict:
        """
        Get current price for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dictionary with current price data
        """
        if not self.mt5_connected:
            return {}
        
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"Failed to get tick for {symbol}")
                return {}
            
            return {
                'symbol': symbol,
                'bid': tick.bid,
                'ask': tick.ask,
                'last': tick.last,
                'volume': tick.volume,
                'time': datetime.fromtimestamp(tick.time),
                'spread': tick.ask - tick.bid,
                'price': (tick.bid + tick.ask) / 2  # Mid price
            }
            
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            return {}
    
    def get_historical_data(self, symbol: str, timeframe: str, count: int = 1000) -> pd.DataFrame:
        """
        Get historical OHLCV data
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
            count: Number of bars to retrieve
            
        Returns:
            DataFrame with OHLCV data
        """
        if not self.mt5_connected:
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
            
            if timeframe not in timeframe_map:
                logger.error(f"Invalid timeframe: {timeframe}")
                return pd.DataFrame()
            
            mt5_timeframe = timeframe_map[timeframe]
            
            # Get historical data
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
            if rates is None:
                logger.error(f"Failed to get historical data for {symbol}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            # Rename columns to match expected format
            df.columns = ['Open', 'High', 'Low', 'Close', 'tick_volume', 'spread', 'real_volume']
            
            # Keep only OHLCV columns
            df = df[['Open', 'High', 'Low', 'Close', 'tick_volume']].copy()
            df.rename(columns={'tick_volume': 'Volume'}, inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            return pd.DataFrame()
    
    def get_account_info(self) -> Dict:
        """
        Get account information
        
        Returns:
            Dictionary with account information
        """
        if not self.mt5_connected or self.account_info is None:
            return {}
        
        return {
            'login': self.account_info.login,
            'trade_mode': self.account_info.trade_mode,
            'leverage': self.account_info.leverage,
            'limit_orders': self.account_info.limit_orders,
            'margin_so_mode': self.account_info.margin_so_mode,
            'trade_allowed': self.account_info.trade_allowed,
            'trade_expert': self.account_info.trade_expert,
            'balance': self.account_info.balance,
            'credit': self.account_info.credit,
            'profit': self.account_info.profit,
            'equity': self.account_info.equity,
            'margin': self.account_info.margin,
            'margin_free': self.account_info.margin_free,
            'margin_level': self.account_info.margin_level,
            'currency': self.account_info.currency,
            'server': self.account_info.server,
            'company': self.account_info.company
        }
    
    def get_positions(self) -> pd.DataFrame:
        """
        Get current open positions
        
        Returns:
            DataFrame with position information
        """
        if not self.mt5_connected:
            return pd.DataFrame()
        
        try:
            positions = mt5.positions_get()
            if positions is None:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df['time_update'] = pd.to_datetime(df['time_update'], unit='s')
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return pd.DataFrame()
    
    def get_orders(self) -> pd.DataFrame:
        """
        Get current pending orders
        
        Returns:
            DataFrame with order information
        """
        if not self.mt5_connected:
            return pd.DataFrame()
        
        try:
            orders = mt5.orders_get()
            if orders is None:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
            df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
            df['time_expiration'] = pd.to_datetime(df['time_expiration'], unit='s')
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting orders: {str(e)}")
            return pd.DataFrame()
    
    def search_symbols(self, pattern: str) -> List[str]:
        """
        Search for symbols matching a pattern
        
        Args:
            pattern: Search pattern (e.g., 'BTC', 'USD', 'EUR')
            
        Returns:
            List of matching symbol names
        """
        if not self.mt5_connected:
            return []
        
        try:
            pattern_upper = pattern.upper()
            matching_symbols = [
                symbol for symbol in self.available_symbols 
                if pattern_upper in symbol.upper()
            ]
            
            return matching_symbols[:50]  # Limit to 50 results
            
        except Exception as e:
            logger.error(f"Error searching symbols: {str(e)}")
            return []
    
    def disconnect(self):
        """
        Disconnect from MetaTrader 5
        """
        if self.mt5_connected:
            mt5.shutdown()
            self.mt5_connected = False
            logger.info("Disconnected from MetaTrader 5")

class MetaTraderStreamlitUI:
    """
    Streamlit UI components for MetaTrader integration
    """
    
    @staticmethod
    def render_connection_form():
        """
        Render MetaTrader connection form
        
        Returns:
            Tuple of (login, password, server) or None if not submitted
        """
        st.sidebar.header("🔗 MetaTrader 5 Connection")
        
        # Connection status
        if 'mt5_provider' in st.session_state and st.session_state.mt5_provider.mt5_connected:
            st.sidebar.success("✅ Connected to MT5")
            
            # Account info
            if hasattr(st.session_state.mt5_provider, 'account_info') and st.session_state.mt5_provider.account_info:
                account = st.session_state.mt5_provider.account_info
                st.sidebar.info(f"Account: {account.login}")
                st.sidebar.info(f"Server: {account.server}")
                st.sidebar.info(f"Balance: {account.balance} {account.currency}")
            
            # Disconnect button
            if st.sidebar.button("Disconnect"):
                st.session_state.mt5_provider.disconnect()
                st.experimental_rerun()
        else:
            st.sidebar.warning("⚠️ Not connected to MT5")
            
            # Connection form
            with st.sidebar.form("mt5_connection"):
                st.write("**Connection Details:**")
                login = st.number_input("Login", min_value=1, value=None, format="%d")
                password = st.text_input("Password", type="password")
                server = st.text_input("Server", placeholder="e.g., MetaQuotes-Demo")
                
                submitted = st.form_submit_button("Connect")
                
                if submitted:
                    if login and password and server:
                        return (int(login), password, server)
                    else:
                        st.error("Please fill in all connection details")
        
        return None
    
    @staticmethod
    def render_symbol_selector(mt5_provider: MetaTraderDataProvider):
        """
        Render symbol selection interface
        
        Args:
            mt5_provider: MetaTrader data provider instance
            
        Returns:
            Selected symbol or None
        """
        st.sidebar.header("📊 Symbol Selection")
        
        if not mt5_provider.mt5_connected:
            st.sidebar.error("Please connect to MT5 first")
            return None
        
        # Search for symbols
        search_term = st.sidebar.text_input("Search symbols", placeholder="e.g., BTC, EUR, USD")
        
        if search_term:
            matching_symbols = mt5_provider.search_symbols(search_term)
            if matching_symbols:
                selected_symbol = st.sidebar.selectbox(
                    "Select Symbol",
                    options=matching_symbols,
                    index=0
                )
                return selected_symbol
            else:
                st.sidebar.warning(f"No symbols found matching '{search_term}'")
        
        # Default common symbols
        common_symbols = ["BTCUSD", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
        available_common = [s for s in common_symbols if s in mt5_provider.available_symbols]
        
        if available_common:
            selected_symbol = st.sidebar.selectbox(
                "Common Symbols",
                options=available_common,
                index=0
            )
            return selected_symbol
        
        return None
    
    @staticmethod
    def render_timeframe_selector():
        """
        Render timeframe selection
        
        Returns:
            Selected timeframe
        """
        timeframes = {
            "1 Minute": "M1",
            "5 Minutes": "M5",
            "15 Minutes": "M15",
            "30 Minutes": "M30",
            "1 Hour": "H1",
            "4 Hours": "H4",
            "1 Day": "D1",
            "1 Week": "W1",
            "1 Month": "MN1"
        }
        
        selected_tf = st.sidebar.selectbox(
            "Timeframe",
            options=list(timeframes.keys()),
            index=4  # Default to 1 Hour
        )
        
        return timeframes[selected_tf]
    
    @staticmethod
    def render_account_info(mt5_provider: MetaTraderDataProvider):
        """
        Render account information
        
        Args:
            mt5_provider: MetaTrader data provider instance
        """
        if not mt5_provider.mt5_connected:
            return
        
        account_info = mt5_provider.get_account_info()
        if not account_info:
            return
        
        st.sidebar.header("💼 Account Info")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Balance", f"{account_info['balance']:.2f}")
            st.metric("Equity", f"{account_info['equity']:.2f}")
        
        with col2:
            st.metric("Margin", f"{account_info['margin']:.2f}")
            st.metric("Free Margin", f"{account_info['margin_free']:.2f}")
        
        if account_info['margin'] > 0:
            margin_level = (account_info['equity'] / account_info['margin']) * 100
            st.sidebar.metric("Margin Level", f"{margin_level:.1f}%")

# Example usage and integration functions
def integrate_with_existing_app():
    """
    Example of how to integrate MetaTrader data with existing Bitcoin analyzer
    """
    # Initialize MetaTrader provider
    if 'mt5_provider' not in st.session_state:
        st.session_state.mt5_provider = MetaTraderDataProvider()
    
    mt5_provider = st.session_state.mt5_provider
    
    # Render connection UI
    connection_details = MetaTraderStreamlitUI.render_connection_form()
    if connection_details:
        login, password, server = connection_details
        if mt5_provider.initialize_mt5(login, password, server):
            st.success("Successfully connected to MetaTrader 5!")
            st.experimental_rerun()
        else:
            st.error("Failed to connect to MetaTrader 5")
    
    # If connected, show trading interface
    if mt5_provider.mt5_connected:
        # Symbol selection
        selected_symbol = MetaTraderStreamlitUI.render_symbol_selector(mt5_provider)
        
        if selected_symbol:
            # Timeframe selection
            timeframe = MetaTraderStreamlitUI.render_timeframe_selector()
            
            # Get data
            current_price = mt5_provider.get_current_price(selected_symbol)
            historical_data = mt5_provider.get_historical_data(selected_symbol, timeframe)
            
            # Display current price
            if current_price:
                st.metric(
                    f"{selected_symbol} Price",
                    f"{current_price['price']:.5f}",
                    f"Spread: {current_price['spread']:.5f}"
                )
            
            # Display historical data
            if not historical_data.empty:
                st.subheader(f"{selected_symbol} - {timeframe} Chart")
                st.line_chart(historical_data['Close'])
                
                # Show data table
                with st.expander("View Raw Data"):
                    st.dataframe(historical_data.tail(50))
        
        # Account info
        MetaTraderStreamlitUI.render_account_info(mt5_provider)
        
        # Positions and orders
        positions = mt5_provider.get_positions()
        if not positions.empty:
            st.subheader("📈 Open Positions")
            st.dataframe(positions[['symbol', 'type', 'volume', 'price_open', 'price_current', 'profit']])
        
        orders = mt5_provider.get_orders()
        if not orders.empty:
            st.subheader("📋 Pending Orders")
            st.dataframe(orders[['symbol', 'type', 'volume', 'price_open', 'time_setup']])

if __name__ == "__main__":
    # Test the MetaTrader integration
    integrate_with_existing_app()