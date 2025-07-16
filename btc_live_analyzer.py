import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
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

# Try to import TA-Lib, fall back to basic indicators if not available
try:
    import talib
    HAS_TALIB = True
    st.sidebar.success("✅ Full version - TA-Lib available")
except ImportError:
    HAS_TALIB = False
    st.sidebar.warning("⚠️ Lite version - Using basic indicators")

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

# Set page config
st.set_page_config(
    page_title="Bitcoin Live Analyzer & Predictor",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .indicator-positive {
        color: #00ff88;
        font-weight: bold;
    }
    .indicator-negative {
        color: #ff4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class BitcoinAnalyzer:
    def __init__(self):
        self.data = None
        self.scaler = StandardScaler()
        self.model = None
        self.features = []
        
    def fetch_binance_data(self, symbol='BTCUSDT', interval='5m', limit=1000):
        """Fetch live data from Binance API"""
        try:
            url = f"https://api.binance.com/api/v3/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'count', 'taker_buy_volume',
                'taker_buy_quote_volume', 'ignore'
            ])
            
            # Convert to proper data types
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_columns] = df[numeric_columns].astype(float)
            
            return df
            
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return None
    
    def calculate_technical_indicators(self, df):
        """Calculate technical indicators (TA-Lib or basic fallback)"""
        if df is None or len(df) < 50:
            return df
        
        if HAS_TALIB:
            # Use TA-Lib for advanced indicators
            df['sma_20'] = talib.SMA(df['close'], timeperiod=20)
            df['sma_50'] = talib.SMA(df['close'], timeperiod=50)
            df['ema_12'] = talib.EMA(df['close'], timeperiod=12)
            df['ema_26'] = talib.EMA(df['close'], timeperiod=26)
            df['macd'], df['macd_signal'], df['macd_histogram'] = talib.MACD(df['close'])
            df['rsi'] = talib.RSI(df['close'], timeperiod=14)
            df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(df['close'])
            df['stoch_k'], df['stoch_d'] = talib.STOCH(df['high'], df['low'], df['close'])
            df['adx'] = talib.ADX(df['high'], df['low'], df['close'])
            df['williams_r'] = talib.WILLR(df['high'], df['low'], df['close'])
            df['volume_sma'] = talib.SMA(df['volume'], timeperiod=20)
            df['ad'] = talib.AD(df['high'], df['low'], df['close'], df['volume'])
            df['obv'] = talib.OBV(df['close'], df['volume'])
            
            # Candlestick patterns
            df['doji'] = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
            df['hammer'] = talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
            df['engulfing'] = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
            
        else:
            # Use basic indicators as fallback
            df['sma_20'] = calculate_sma(df['close'], 20)
            df['sma_50'] = calculate_sma(df['close'], 50)
            df['ema_12'] = calculate_ema(df['close'], 12)
            df['ema_26'] = calculate_ema(df['close'], 26)
            df['macd'], df['macd_signal'], df['macd_histogram'] = calculate_macd(df['close'])
            df['rsi'] = calculate_rsi(df['close'])
            df['bb_upper'], df['bb_middle'], df['bb_lower'] = calculate_bollinger_bands(df['close'])
            df['stoch_k'], df['stoch_d'] = calculate_stochastic(df['high'], df['low'], df['close'])
            df['volume_sma'] = calculate_sma(df['volume'], 20)
        
        # Common indicators for both versions
        df['price_change'] = df['close'].pct_change()
        df['volatility'] = df['price_change'].rolling(window=20).std()
        df['support_resistance'] = df['close'].rolling(window=20).apply(
            lambda x: (x.iloc[-1] - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 0.5
        )
        
        return df
    
    def prepare_features(self, df):
        """Prepare features for machine learning"""
        if df is None:
            return None, None
        
        # Select available features
        if HAS_TALIB:
            feature_columns = [
                'sma_20', 'sma_50', 'ema_12', 'ema_26', 'macd', 'macd_signal',
                'rsi', 'bb_upper', 'bb_middle', 'bb_lower', 'stoch_k', 'stoch_d',
                'adx', 'williams_r', 'volume_sma', 'volatility', 'support_resistance'
            ]
        else:
            feature_columns = [
                'sma_20', 'sma_50', 'ema_12', 'ema_26', 'macd', 'macd_signal',
                'rsi', 'bb_upper', 'bb_middle', 'bb_lower', 'stoch_k', 'stoch_d',
                'volume_sma', 'volatility', 'support_resistance'
            ]
        
        # Create target variable (next candle direction)
        df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
        
        # Remove NaN values
        df_clean = df.dropna()
        
        if len(df_clean) < 50:
            return None, None
        
        # Only use columns that exist
        available_features = [col for col in feature_columns if col in df_clean.columns]
        
        X = df_clean[available_features]
        y = df_clean['target']
        
        return X, y
    
    def train_model(self, X, y):
        """Train machine learning model"""
        if X is None or y is None or len(X) < 50:
            return None, None, None
        
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train ensemble model
            gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            
            gb_model.fit(X_train_scaled, y_train)
            rf_model.fit(X_train_scaled, y_train)
            
            # Ensemble prediction
            gb_pred = gb_model.predict_proba(X_test_scaled)[:, 1]
            rf_pred = rf_model.predict_proba(X_test_scaled)[:, 1]
            
            ensemble_pred = (gb_pred + rf_pred) / 2
            ensemble_pred_class = (ensemble_pred > 0.5).astype(int)
            
            accuracy = accuracy_score(y_test, ensemble_pred_class)
            
            self.model = {'gb': gb_model, 'rf': rf_model}
            
            return accuracy, ensemble_pred_class, y_test
            
        except Exception as e:
            st.error(f"Model training error: {str(e)}")
            return None, None, None
    
    def predict_next_candle(self, df):
        """Predict next candle direction"""
        if self.model is None or df is None:
            return None, None
        
        try:
            # Get latest features
            X, _ = self.prepare_features(df)
            if X is None:
                return None, None
            
            # Use last row for prediction
            X_latest = X.iloc[-1:].values
            X_scaled = self.scaler.transform(X_latest)
            
            # Ensemble prediction
            gb_prob = self.model['gb'].predict_proba(X_scaled)[0, 1]
            rf_prob = self.model['rf'].predict_proba(X_scaled)[0, 1]
            
            ensemble_prob = (gb_prob + rf_prob) / 2
            prediction = 1 if ensemble_prob > 0.5 else 0
            
            return prediction, ensemble_prob
            
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            return None, None

def create_candlestick_chart(df, indicators=True):
    """Create interactive candlestick chart"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Price & Indicators', 'Volume', 'Technical Indicators'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='BTCUSDT',
            increasing_line_color='#00ff88',
            decreasing_line_color='#ff4444'
        ),
        row=1, col=1
    )
    
    if indicators and 'sma_20' in df.columns:
        # Moving averages
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['sma_20'], name='SMA 20', line=dict(color='orange')),
            row=1, col=1
        )
        if 'sma_50' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['sma_50'], name='SMA 50', line=dict(color='purple')),
                row=1, col=1
            )
        
        # Bollinger Bands
        if 'bb_upper' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['bb_upper'], name='BB Upper', 
                          line=dict(color='gray', dash='dash'), opacity=0.7),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df['bb_lower'], name='BB Lower', 
                          line=dict(color='gray', dash='dash'), opacity=0.7),
                row=1, col=1
            )
    
    # Volume
    colors = ['#00ff88' if row['close'] >= row['open'] else '#ff4444' for _, row in df.iterrows()]
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['volume'], name='Volume', marker_color=colors),
        row=2, col=1
    )
    
    # RSI
    if 'rsi' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['rsi'], name='RSI', line=dict(color='cyan')),
            row=3, col=1
        )
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    fig.update_layout(
        title=f'Bitcoin (BTC/USDT) Live Analysis {"(Full)" if HAS_TALIB else "(Lite)"}',
        height=800,
        showlegend=True,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig

def create_prediction_gauge(prediction_prob, prediction):
    """Create prediction gauge chart"""
    if prediction_prob is None or prediction is None:
        # Create empty gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=50,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "No Prediction Available"},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "gray"}}
        ))
    else:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=prediction_prob * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Next Candle: {'🟢 UP' if prediction == 1 else '🔴 DOWN'}"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00ff88" if prediction == 1 else "#ff4444"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        font={'color': "white", 'family': "Arial"}
    )
    
    return fig

def main():
    st.markdown("<h1 class='main-header'>₿ Bitcoin Live Analyzer & Predictor</h1>", unsafe_allow_html=True)
    
    # Show version info
    if HAS_TALIB:
        st.success("🚀 Full Version - All indicators available!")
    else:
        st.info("⚡ Lite Version - Basic indicators (still powerful!)")
    
    # Initialize analyzer
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = BitcoinAnalyzer()
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh", value=True)
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 60)
    
    # Data settings
    st.sidebar.subheader("📊 Data Settings")
    data_limit = st.sidebar.slider("Data Points", 100, 1000, 500)
    
    # Prediction settings
    st.sidebar.subheader("🎯 Prediction Settings")
    retrain_model = st.sidebar.button("🔄 Retrain Model")
    
    # Model performance
    if 'model_accuracy' in st.session_state:
        st.sidebar.metric("Model Accuracy", f"{st.session_state.model_accuracy:.2%}")
    
    # Main content
    col1, col2, col3 = st.columns([2, 1, 1])
    
    # Fetch and process data
    with st.spinner("Fetching live Bitcoin data..."):
        df = st.session_state.analyzer.fetch_binance_data(limit=data_limit)
        
        if df is not None:
            df = st.session_state.analyzer.calculate_technical_indicators(df)
            
            # Current price info
            current_price = df['close'].iloc[-1]
            price_change = df['close'].iloc[-1] - df['close'].iloc[-2]
            price_change_pct = (price_change / df['close'].iloc[-2]) * 100
            
            with col1:
                st.metric(
                    "Current Price",
                    f"${current_price:,.2f}",
                    f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
                )
            
            with col2:
                volume_24h = df['volume'].iloc[-24:].sum() if len(df) >= 24 else df['volume'].sum()
                st.metric("Volume", f"{volume_24h/1000:.1f}K BTC")
            
            with col3:
                volatility = df['volatility'].iloc[-1] if 'volatility' in df.columns and not pd.isna(df['volatility'].iloc[-1]) else 0
                st.metric("Volatility", f"{volatility:.4f}")
            
            # Train model if needed
            if retrain_model or 'model_accuracy' not in st.session_state:
                with st.spinner("Training prediction model..."):
                    X, y = st.session_state.analyzer.prepare_features(df)
                    if X is not None and y is not None:
                        accuracy, pred, actual = st.session_state.analyzer.train_model(X, y)
                        if accuracy is not None:
                            st.session_state.model_accuracy = accuracy
                            st.success(f"Model trained with {accuracy:.2%} accuracy!")
                        else:
                            st.warning("Model training failed - insufficient data")
                    else:
                        st.warning("Insufficient data for model training")
            
            # Make prediction
            prediction, prediction_prob = st.session_state.analyzer.predict_next_candle(df)
            
            # Main chart
            st.subheader("📈 Live Price Chart")
            chart = create_candlestick_chart(df)
            st.plotly_chart(chart, use_container_width=True)
            
            # Prediction section
            col_pred1, col_pred2 = st.columns([1, 1])
            
            with col_pred1:
                st.subheader("🔮 Next Candle Prediction")
                gauge_chart = create_prediction_gauge(prediction_prob, prediction)
                st.plotly_chart(gauge_chart, use_container_width=True)
            
            with col_pred2:
                st.subheader("📊 Technical Analysis")
                
                # Current indicators
                if 'rsi' in df.columns and not pd.isna(df['rsi'].iloc[-1]):
                    rsi_current = df['rsi'].iloc[-1]
                    rsi_status = "Overbought" if rsi_current > 70 else "Oversold" if rsi_current < 30 else "Normal"
                    st.metric("RSI", f"{rsi_current:.2f}", rsi_status)
                
                if 'macd' in df.columns and not pd.isna(df['macd'].iloc[-1]):
                    macd_current = df['macd'].iloc[-1]
                    macd_signal = df['macd_signal'].iloc[-1]
                    macd_status = "Bullish" if macd_current > macd_signal else "Bearish"
                    st.metric("MACD", f"{macd_current:.4f}", macd_status)
                
                if 'stoch_k' in df.columns and not pd.isna(df['stoch_k'].iloc[-1]):
                    stoch_current = df['stoch_k'].iloc[-1]
                    stoch_status = "Overbought" if stoch_current > 80 else "Oversold" if stoch_current < 20 else "Normal"
                    st.metric("Stochastic", f"{stoch_current:.2f}", stoch_status)
            
            # Additional analysis
            st.subheader("🔍 Market Analysis")
            
            col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
            
            with col_analysis1:
                st.markdown("### Trend Analysis")
                if 'sma_20' in df.columns and 'sma_50' in df.columns:
                    sma20 = df['sma_20'].iloc[-1]
                    sma50 = df['sma_50'].iloc[-1]
                    if not pd.isna(sma20) and not pd.isna(sma50):
                        trend = "Uptrend" if sma20 > sma50 else "Downtrend"
                        st.write(f"**Trend**: {trend}")
                        st.write(f"**SMA 20**: ${sma20:.2f}")
                        st.write(f"**SMA 50**: ${sma50:.2f}")
            
            with col_analysis2:
                st.markdown("### Volume Analysis")
                current_volume = df['volume'].iloc[-1]
                if 'volume_sma' in df.columns and not pd.isna(df['volume_sma'].iloc[-1]):
                    avg_volume = df['volume_sma'].iloc[-1]
                    volume_ratio = current_volume / avg_volume
                    st.write(f"**Current Volume**: {current_volume:.0f}")
                    st.write(f"**Avg Volume**: {avg_volume:.0f}")
                    st.write(f"**Volume Ratio**: {volume_ratio:.2f}x")
                else:
                    st.write(f"**Current Volume**: {current_volume:.0f}")
            
            with col_analysis3:
                st.markdown("### Price Levels")
                if 'bb_upper' in df.columns and 'bb_lower' in df.columns:
                    bb_upper = df['bb_upper'].iloc[-1]
                    bb_lower = df['bb_lower'].iloc[-1]
                    if not pd.isna(bb_upper) and not pd.isna(bb_lower):
                        bb_width = ((bb_upper - bb_lower) / current_price) * 100
                        st.write(f"**Resistance**: ${bb_upper:.2f}")
                        st.write(f"**Support**: ${bb_lower:.2f}")
                        st.write(f"**BB Width**: {bb_width:.2f}%")
        
        else:
            st.error("Failed to fetch data. Please check your connection.")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
