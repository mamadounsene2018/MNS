"""
Trend analysis for stock price movements
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional


class TrendAnalyzer:
    """
    Analyze trends in stock prices and trading volumes
    
    Includes:
    - Moving averages (SMA, EMA)
    - Trend identification
    - Support and resistance levels
    - Momentum indicators
    """
    
    def __init__(self, stock_data: pd.DataFrame):
        """
        Initialize with stock price data
        
        Args:
            stock_data: DataFrame with stock price data (must have 'Close' column)
        """
        self.data = stock_data.copy()
        
        if 'Close' not in self.data.columns:
            raise ValueError("Stock data must contain 'Close' column")
    
    def calculate_sma(self, period: int = 20, column: str = 'Close') -> pd.Series:
        """
        Calculate Simple Moving Average
        
        Args:
            period: Number of periods for SMA
            column: Column to calculate SMA on
            
        Returns:
            Series with SMA values
        """
        return self.data[column].rolling(window=period).mean()
    
    def calculate_ema(self, period: int = 20, column: str = 'Close') -> pd.Series:
        """
        Calculate Exponential Moving Average
        
        Args:
            period: Number of periods for EMA
            column: Column to calculate EMA on
            
        Returns:
            Series with EMA values
        """
        return self.data[column].ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, period: int = 14, column: str = 'Close') -> pd.Series:
        """
        Calculate Relative Strength Index
        
        Args:
            period: Number of periods for RSI (typically 14)
            column: Column to calculate RSI on
            
        Returns:
            Series with RSI values (0-100)
        """
        delta = self.data[column].diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(
        self, 
        fast_period: int = 12, 
        slow_period: int = 26, 
        signal_period: int = 9,
        column: str = 'Close'
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line period
            column: Column to calculate MACD on
            
        Returns:
            Tuple of (MACD line, Signal line, MACD histogram)
        """
        fast_ema = self.data[column].ewm(span=fast_period, adjust=False).mean()
        slow_ema = self.data[column].ewm(span=slow_period, adjust=False).mean()
        
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def calculate_bollinger_bands(
        self, 
        period: int = 20, 
        std_dev: float = 2.0,
        column: str = 'Close'
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands
        
        Args:
            period: Period for moving average
            std_dev: Number of standard deviations for bands
            column: Column to calculate bands on
            
        Returns:
            Tuple of (Middle band, Upper band, Lower band)
        """
        middle_band = self.data[column].rolling(window=period).mean()
        std = self.data[column].rolling(window=period).std()
        
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        
        return middle_band, upper_band, lower_band
    
    def identify_trend(self, window: int = 50) -> str:
        """
        Identify current price trend
        
        Args:
            window: Number of periods to consider for trend
            
        Returns:
            String describing the trend ('Uptrend', 'Downtrend', 'Sideways')
        """
        if len(self.data) < window:
            return 'Insufficient data'
        
        recent_data = self.data['Close'].tail(window)
        
        # Calculate linear regression slope
        x = np.arange(len(recent_data))
        y = recent_data.values
        
        slope = np.polyfit(x, y, 1)[0]
        
        # Determine trend based on slope
        if slope > 0.1:
            return 'Uptrend'
        elif slope < -0.1:
            return 'Downtrend'
        else:
            return 'Sideways'
    
    def get_support_resistance(
        self, 
        window: int = 20, 
        num_levels: int = 3
    ) -> Tuple[list, list]:
        """
        Identify support and resistance levels
        
        Args:
            window: Window for identifying local extrema
            num_levels: Number of support/resistance levels to identify
            
        Returns:
            Tuple of (support_levels, resistance_levels)
        """
        highs = self.data['High'].rolling(window=window, center=True).max()
        lows = self.data['Low'].rolling(window=window, center=True).min()
        
        # Find local maxima (resistance)
        resistance_points = self.data[self.data['High'] == highs]['High'].values
        
        # Find local minima (support)
        support_points = self.data[self.data['Low'] == lows]['Low'].values
        
        # Get unique levels and sort
        resistance_levels = sorted(set(resistance_points), reverse=True)[:num_levels]
        support_levels = sorted(set(support_points))[:num_levels]
        
        return support_levels, resistance_levels
    
    def get_momentum_score(self) -> float:
        """
        Calculate overall momentum score (-100 to 100)
        
        Returns:
            Momentum score
        """
        # Calculate RSI
        rsi = self.calculate_rsi()
        current_rsi = rsi.iloc[-1] if not rsi.empty and len(rsi) > 0 else 50
        
        # Calculate MACD
        macd_line, signal_line, _ = self.calculate_macd()
        macd_signal = 0
        if not macd_line.empty and not signal_line.empty and len(macd_line) > 0 and len(signal_line) > 0:
            macd_signal = 1 if macd_line.iloc[-1] > signal_line.iloc[-1] else -1
        
        # Calculate price position relative to moving averages
        sma_20 = self.calculate_sma(20)
        sma_50 = self.calculate_sma(50)
        
        current_price = self.data['Close'].iloc[-1] if len(self.data) > 0 else 0
        sma_score = 0
        
        if not sma_20.empty and not pd.isna(sma_20.iloc[-1]):
            if current_price > sma_20.iloc[-1]:
                sma_score += 1
            else:
                sma_score -= 1
        
        if not sma_50.empty and not pd.isna(sma_50.iloc[-1]):
            if current_price > sma_50.iloc[-1]:
                sma_score += 1
            else:
                sma_score -= 1
        
        # Combine indicators
        rsi_score = (current_rsi - 50) / 50  # Normalize to -1 to 1
        momentum = (rsi_score + macd_signal + sma_score) / 4 * 100
        
        return momentum
    
    def get_analysis_summary(self) -> str:
        """
        Get a comprehensive analysis summary
        
        Returns:
            Formatted string with analysis summary
        """
        if len(self.data) == 0:
            return "No data available for analysis"
        
        trend = self.identify_trend()
        momentum = self.get_momentum_score()
        
        # Get latest values
        current_price = self.data['Close'].iloc[-1]
        sma_20 = self.calculate_sma(20).iloc[-1] if len(self.calculate_sma(20)) > 0 else None
        sma_50 = self.calculate_sma(50).iloc[-1] if len(self.calculate_sma(50)) > 0 else None
        rsi = self.calculate_rsi().iloc[-1] if len(self.calculate_rsi()) > 0 else None
        
        summary = "=== Technical Analysis Summary ===\n"
        summary += f"Current Price: {current_price:.2f}\n"
        summary += f"Trend: {trend}\n"
        summary += f"Momentum Score: {momentum:.2f}\n\n"
        
        summary += "=== Moving Averages ===\n"
        if not pd.isna(sma_20):
            summary += f"SMA 20: {sma_20:.2f}\n"
        if not pd.isna(sma_50):
            summary += f"SMA 50: {sma_50:.2f}\n"
        
        summary += f"\n=== Indicators ===\n"
        if not pd.isna(rsi):
            summary += f"RSI (14): {rsi:.2f}\n"
            
            if rsi > 70:
                summary += "  -> Overbought territory\n"
            elif rsi < 30:
                summary += "  -> Oversold territory\n"
            else:
                summary += "  -> Neutral\n"
        
        return summary
