import streamlit as st

# Set page config FIRST - before any other Streamlit commands
st.set_page_config(
    page_title="Bitcoin Live Analyzer & Predictor - MT5 Edition",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Machine Learning imports
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from typing import Dict, List, Tuple

# MetaTrader integration
from mt5_integration import MetaTraderDataProvider, MetaTraderStreamlitUI

# Try to import TA-Lib, fall back to basic indicators if not available
try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False

# Basic technical indicators for fallback
def calculate_sma(data, window):
    """Simple Moving Average"""
    return data.rolling(window=window).mean()

def calculate_ema(data, window):
    """Exponential Moving Average"""
    return data.ewm(span=window).mean()

def calculate_rsi(data, window=14):
    """Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Bollinger Bands"""
    rolling_mean = data.rolling(window=window).mean()
    rolling_std = data.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, rolling_mean, lower_band

def calculate_macd(data, fast=12, slow=26, signal=9):
    """MACD Indicator"""
    ema_fast = calculate_ema(data, fast)
    ema_slow = calculate_ema(data, slow)
    macd = ema_fast - ema_slow
    macd_signal = calculate_ema(macd, signal)
    macd_histogram = macd - macd_signal
    return macd, macd_signal, macd_histogram

def calculate_stochastic(high, low, close, k_window=14, d_window=3):
    """Stochastic Oscillator"""
    lowest_low = low.rolling(window=k_window).min()
    highest_high = high.rolling(window=k_window).max()
    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d_percent = k_percent.rolling(window=d_window).mean()
    return k_percent, d_percent

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #f7931a;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metric-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .stMetric {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

class MetaTraderBitcoinAnalyzer:
    """
    Enhanced Bitcoin analyzer with MetaTrader 5 integration
    """
    
    def __init__(self):
        self.mt5_provider = None
        self.current_symbol = None
        self.current_timeframe = None
        self.data = pd.DataFrame()
        self.model = None
        self.scaler = None
        
    def initialize_mt5_connection(self):
        """Initialize MetaTrader 5 connection"""
        if 'mt5_provider' not in st.session_state:
            st.session_state.mt5_provider = MetaTraderDataProvider()
        
        self.mt5_provider = st.session_state.mt5_provider
        return self.mt5_provider.mt5_connected
    
    def get_mt5_data(self, symbol: str, timeframe: str, count: int = 1000):
        """Get data from MetaTrader 5"""
        if not self.mt5_provider or not self.mt5_provider.mt5_connected:
            return pd.DataFrame()
        
        try:
            # Get historical data
            df = self.mt5_provider.get_historical_data(symbol, timeframe, count)
            
            if df.empty:
                st.error(f"No data available for {symbol} on {timeframe}")
                return pd.DataFrame()
            
            # Store current symbol and timeframe
            self.current_symbol = symbol
            self.current_timeframe = timeframe
            
            return df
            
        except Exception as e:
            st.error(f"Error getting MT5 data: {str(e)}")
            return pd.DataFrame()
    
    def add_technical_indicators(self, df):
        """Add technical indicators to the dataframe"""
        if df.empty:
            return df
        
        try:
            # Use TA-Lib if available, otherwise use basic indicators
            if HAS_TALIB:
                # TA-Lib indicators
                df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
                df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
                df['EMA_12'] = talib.EMA(df['Close'], timeperiod=12)
                df['EMA_26'] = talib.EMA(df['Close'], timeperiod=26)
                df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
                df['MACD'], df['MACD_signal'], df['MACD_histogram'] = talib.MACD(df['Close'])
                df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(df['Close'])
                df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
                df['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
                df['CCI'] = talib.CCI(df['High'], df['Low'], df['Close'], timeperiod=14)
                df['MFI'] = talib.MFI(df['High'], df['Low'], df['Close'], df['Volume'], timeperiod=14)
                df['WILLR'] = talib.WILLR(df['High'], df['Low'], df['Close'], timeperiod=14)
                df['STOCH_K'], df['STOCH_D'] = talib.STOCH(df['High'], df['Low'], df['Close'])
            else:
                # Basic indicators
                df['SMA_20'] = calculate_sma(df['Close'], 20)
                df['SMA_50'] = calculate_sma(df['Close'], 50)
                df['EMA_12'] = calculate_ema(df['Close'], 12)
                df['EMA_26'] = calculate_ema(df['Close'], 26)
                df['RSI'] = calculate_rsi(df['Close'])
                df['MACD'], df['MACD_signal'], df['MACD_histogram'] = calculate_macd(df['Close'])
                df['BB_upper'], df['BB_middle'], df['BB_lower'] = calculate_bollinger_bands(df['Close'])
                df['STOCH_K'], df['STOCH_D'] = calculate_stochastic(df['High'], df['Low'], df['Close'])
            
            # Additional calculated indicators
            df['Price_Change'] = df['Close'].pct_change()
            df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
            df['High_Low_Ratio'] = df['High'] / df['Low']
            df['Price_Range'] = df['High'] - df['Low']
            
            return df
            
        except Exception as e:
            st.error(f"Error adding technical indicators: {str(e)}")
            return df
    
    def create_features_for_ml(self, df):
        """Create features for machine learning"""
        if df.empty:
            return pd.DataFrame()
        
        try:
            features = pd.DataFrame(index=df.index)
            
            # Price features
            features['close'] = df['Close']
            features['volume'] = df['Volume']
            features['high_low_ratio'] = df['High'] / df['Low']
            features['price_change'] = df['Close'].pct_change()
            features['volume_change'] = df['Volume'].pct_change()
            
            # Technical indicators
            features['rsi'] = df['RSI']
            features['macd'] = df['MACD']
            features['macd_signal'] = df['MACD_signal']
            features['bb_position'] = (df['Close'] - df['BB_lower']) / (df['BB_upper'] - df['BB_lower'])
            features['sma_20'] = df['SMA_20']
            features['sma_50'] = df['SMA_50']
            features['ema_12'] = df['EMA_12']
            features['ema_26'] = df['EMA_26']
            
            # Lag features
            for lag in [1, 2, 3, 5]:
                features[f'close_lag_{lag}'] = df['Close'].shift(lag)
                features[f'volume_lag_{lag}'] = df['Volume'].shift(lag)
                features[f'rsi_lag_{lag}'] = df['RSI'].shift(lag)
            
            # Rolling statistics
            for window in [5, 10, 20]:
                features[f'close_mean_{window}'] = df['Close'].rolling(window).mean()
                features[f'close_std_{window}'] = df['Close'].rolling(window).std()
                features[f'volume_mean_{window}'] = df['Volume'].rolling(window).mean()
            
            # Drop NaN values
            features = features.dropna()
            
            return features
            
        except Exception as e:
            st.error(f"Error creating ML features: {str(e)}")
            return pd.DataFrame()
    
    def train_ml_model(self, df):
        """Train machine learning model for price prediction"""
        if df.empty:
            return None, None
        
        try:
            # Create features
            features = self.create_features_for_ml(df)
            if features.empty:
                return None, None
            
            # Create target (next period's price direction)
            target = (features['close'].shift(-1) > features['close']).astype(int)
            
            # Align features and target
            features = features[:-1]  # Remove last row (no target)
            target = target[:-1]      # Remove last row (NaN)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.2, random_state=42, stratify=target
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            st.info(f"Model trained - Train accuracy: {train_score:.3f}, Test accuracy: {test_score:.3f}")
            
            return model, scaler
            
        except Exception as e:
            st.error(f"Error training ML model: {str(e)}")
            return None, None
    
    def predict_price_direction(self, df, model, scaler):
        """Predict next price direction"""
        if df.empty or model is None or scaler is None:
            return None
        
        try:
            # Create features for the latest data point
            features = self.create_features_for_ml(df)
            if features.empty:
                return None
            
            # Get the latest features
            latest_features = features.iloc[-1:].values
            
            # Scale features
            latest_features_scaled = scaler.transform(latest_features)
            
            # Make prediction
            prediction = model.predict(latest_features_scaled)[0]
            probability = model.predict_proba(latest_features_scaled)[0]
            
            return {
                'direction': 'UP' if prediction == 1 else 'DOWN',
                'probability': max(probability),
                'confidence': 'High' if max(probability) > 0.7 else 'Medium' if max(probability) > 0.6 else 'Low'
            }
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            return None
    
    def create_candlestick_chart(self, df):
        """Create candlestick chart with indicators"""
        if df.empty:
            return None
        
        try:
            # Create subplots
            fig = make_subplots(
                rows=4, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=(f'{self.current_symbol} Price', 'Volume', 'RSI', 'MACD'),
                row_heights=[0.5, 0.2, 0.15, 0.15]
            )
            
            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Price'
                ),
                row=1, col=1
            )
            
            # Add moving averages
            fig.add_trace(
                go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='orange')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='red')),
                row=1, col=1
            )
            
            # Bollinger Bands
            fig.add_trace(
                go.Scatter(x=df.index, y=df['BB_upper'], name='BB Upper', line=dict(color='gray', dash='dash')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['BB_lower'], name='BB Lower', line=dict(color='gray', dash='dash')),
                row=1, col=1
            )
            
            # Volume
            fig.add_trace(
                go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='lightblue'),
                row=2, col=1
            )
            
            # RSI
            fig.add_trace(
                go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')),
                row=3, col=1
            )
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
            
            # MACD
            fig.add_trace(
                go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')),
                row=4, col=1
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['MACD_signal'], name='Signal', line=dict(color='red')),
                row=4, col=1
            )
            fig.add_trace(
                go.Bar(x=df.index, y=df['MACD_histogram'], name='Histogram', marker_color='gray'),
                row=4, col=1
            )
            
            # Update layout
            fig.update_layout(
                title=f'{self.current_symbol} - {self.current_timeframe} Analysis',
                xaxis_rangeslider_visible=False,
                height=800,
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
            return None

def main():
    st.markdown("<h1 class='main-header'>₿ Bitcoin Live Analyzer & Predictor - MT5 Edition</h1>", unsafe_allow_html=True)
    
    # Show version info
    if HAS_TALIB:
        st.success("🚀 Full Version - All indicators available!")
    else:
        st.info("⚡ Lite Version - Basic indicators (still powerful!)")
    
    # Initialize analyzer
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = MetaTraderBitcoinAnalyzer()
    
    analyzer = st.session_state.analyzer
    
    # Initialize MetaTrader connection
    analyzer.initialize_mt5_connection()
    
    # Sidebar - MetaTrader Connection
    connection_details = MetaTraderStreamlitUI.render_connection_form()
    if connection_details:
        login, password, server = connection_details
        if analyzer.mt5_provider.initialize_mt5(login, password, server):
            st.success("Successfully connected to MetaTrader 5!")
            st.experimental_rerun()
        else:
            st.error("Failed to connect to MetaTrader 5")
    
    # Main content
    if analyzer.mt5_provider and analyzer.mt5_provider.mt5_connected:
        # Symbol selection
        selected_symbol = MetaTraderStreamlitUI.render_symbol_selector(analyzer.mt5_provider)
        
        if selected_symbol:
            # Timeframe selection
            timeframe = MetaTraderStreamlitUI.render_timeframe_selector()
            
            # Data count selection
            data_count = st.sidebar.slider("Data Points", min_value=100, max_value=5000, value=1000, step=100)
            
            # Get data button
            if st.sidebar.button("📊 Load Data") or st.sidebar.button("🔄 Refresh Data"):
                with st.spinner("Loading data from MetaTrader 5..."):
                    df = analyzer.get_mt5_data(selected_symbol, timeframe, data_count)
                    
                    if not df.empty:
                        # Add technical indicators
                        df = analyzer.add_technical_indicators(df)
                        analyzer.data = df
                        
                        # Train ML model
                        with st.spinner("Training ML model..."):
                            model, scaler = analyzer.train_ml_model(df)
                            analyzer.model = model
                            analyzer.scaler = scaler
                        
                        st.success(f"Loaded {len(df)} data points for {selected_symbol}")
            
            # Display data if available
            if not analyzer.data.empty:
                # Current price info
                current_price = analyzer.mt5_provider.get_current_price(selected_symbol)
                if current_price:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Current Price", f"{current_price['price']:.5f}")
                    with col2:
                        st.metric("Bid", f"{current_price['bid']:.5f}")
                    with col3:
                        st.metric("Ask", f"{current_price['ask']:.5f}")
                    with col4:
                        st.metric("Spread", f"{current_price['spread']:.5f}")
                
                # ML Prediction
                if analyzer.model and analyzer.scaler:
                    prediction = analyzer.predict_price_direction(analyzer.data, analyzer.model, analyzer.scaler)
                    if prediction:
                        st.markdown(f"""
                        <div class="prediction-box">
                            <h3>🤖 AI Prediction</h3>
                            <p><strong>Direction:</strong> {prediction['direction']}</p>
                            <p><strong>Confidence:</strong> {prediction['confidence']} ({prediction['probability']:.3f})</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Chart
                chart = analyzer.create_candlestick_chart(analyzer.data)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                
                # Technical indicators summary
                latest_data = analyzer.data.iloc[-1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.subheader("📊 Technical Indicators")
                    st.metric("RSI", f"{latest_data['RSI']:.2f}")
                    st.metric("MACD", f"{latest_data['MACD']:.5f}")
                    st.metric("SMA 20", f"{latest_data['SMA_20']:.5f}")
                
                with col2:
                    st.subheader("📈 Moving Averages")
                    st.metric("SMA 50", f"{latest_data['SMA_50']:.5f}")
                    st.metric("EMA 12", f"{latest_data['EMA_12']:.5f}")
                    st.metric("EMA 26", f"{latest_data['EMA_26']:.5f}")
                
                with col3:
                    st.subheader("🎯 Bollinger Bands")
                    st.metric("Upper Band", f"{latest_data['BB_upper']:.5f}")
                    st.metric("Middle Band", f"{latest_data['BB_middle']:.5f}")
                    st.metric("Lower Band", f"{latest_data['BB_lower']:.5f}")
                
                # Raw data
                with st.expander("📋 Raw Data"):
                    st.dataframe(analyzer.data.tail(100))
        
        # Account info
        MetaTraderStreamlitUI.render_account_info(analyzer.mt5_provider)
        
        # Positions and orders
        positions = analyzer.mt5_provider.get_positions()
        if not positions.empty:
            st.subheader("📈 Open Positions")
            st.dataframe(positions[['symbol', 'type', 'volume', 'price_open', 'price_current', 'profit']])
        
        orders = analyzer.mt5_provider.get_orders()
        if not orders.empty:
            st.subheader("📋 Pending Orders")
            st.dataframe(orders[['symbol', 'type', 'volume', 'price_open', 'time_setup']])
    
    else:
        st.warning("Please connect to MetaTrader 5 to start analyzing data.")
        st.info("👆 Use the sidebar to enter your MT5 connection details.")

if __name__ == "__main__":
    main()