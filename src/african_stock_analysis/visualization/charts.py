"""
Chart generation for stock visualization
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple
from datetime import datetime


class ChartGenerator:
    """
    Generate various charts for stock analysis and visualization
    """
    
    def __init__(self):
        """Initialize chart generator with default style"""
        sns.set_style('whitegrid')
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def plot_price_history(
        self, 
        stock_data: pd.DataFrame,
        title: str = "Stock Price History",
        show_volume: bool = True,
        save_path: Optional[str] = None
    ):
        """
        Plot stock price history with optional volume
        
        Args:
            stock_data: DataFrame with stock data (must have 'Close' and optionally 'Volume')
            title: Chart title
            show_volume: Whether to show volume subplot
            save_path: Optional path to save the chart
        """
        if show_volume and 'Volume' in stock_data.columns:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                           gridspec_kw={'height_ratios': [3, 1]})
        else:
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax2 = None
        
        # Plot price
        ax1.plot(stock_data.index, stock_data['Close'], linewidth=2, color='blue', label='Close Price')
        
        if 'High' in stock_data.columns and 'Low' in stock_data.columns:
            ax1.fill_between(stock_data.index, stock_data['Low'], stock_data['High'], 
                            alpha=0.2, color='blue', label='High-Low Range')
        
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Plot volume if requested
        if ax2 is not None and 'Volume' in stock_data.columns:
            # Determine colors based on price movement if Open data is available
            if 'Open' in stock_data.columns:
                colors = ['green' if row['Close'] >= row['Open'] else 'red' 
                         for idx, row in stock_data.iterrows()]
            else:
                colors = 'gray'
            
            ax2.bar(stock_data.index, stock_data['Volume'], color=colors, alpha=0.6)
            ax2.set_ylabel('Volume', fontsize=12)
            ax2.set_xlabel('Date', fontsize=12)
            ax2.grid(True, alpha=0.3)
        else:
            ax1.set_xlabel('Date', fontsize=12)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_moving_averages(
        self,
        stock_data: pd.DataFrame,
        periods: List[int] = [20, 50, 200],
        title: str = "Price with Moving Averages",
        save_path: Optional[str] = None
    ):
        """
        Plot price with multiple moving averages
        
        Args:
            stock_data: DataFrame with stock data
            periods: List of MA periods to plot
            title: Chart title
            save_path: Optional path to save the chart
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot close price
        ax.plot(stock_data.index, stock_data['Close'], 
               linewidth=2, label='Close Price', color='black')
        
        # Plot moving averages
        colors = ['blue', 'orange', 'green', 'red', 'purple']
        for i, period in enumerate(periods):
            ma = stock_data['Close'].rolling(window=period).mean()
            ax.plot(stock_data.index, ma, 
                   linewidth=1.5, label=f'MA {period}', 
                   color=colors[i % len(colors)], alpha=0.7)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_candlestick(
        self,
        stock_data: pd.DataFrame,
        title: str = "Candlestick Chart",
        num_candles: int = 60,
        save_path: Optional[str] = None
    ):
        """
        Plot candlestick chart
        
        Args:
            stock_data: DataFrame with OHLC data
            title: Chart title
            num_candles: Number of recent candles to show
            save_path: Optional path to save the chart
        """
        # Select recent data
        data = stock_data.tail(num_candles).copy()
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Calculate candle positions
        for idx, (index, row) in enumerate(data.iterrows()):
            # Determine color
            color = 'green' if row['Close'] >= row['Open'] else 'red'
            
            # Draw high-low line
            ax.plot([idx, idx], [row['Low'], row['High']], 
                   color=color, linewidth=1)
            
            # Draw open-close box
            height = abs(row['Close'] - row['Open'])
            bottom = min(row['Open'], row['Close'])
            
            ax.add_patch(plt.Rectangle((idx - 0.3, bottom), 0.6, height,
                                      facecolor=color, edgecolor=color, alpha=0.8))
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Trading Days', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_returns_distribution(
        self,
        stock_data: pd.DataFrame,
        title: str = "Returns Distribution",
        save_path: Optional[str] = None
    ):
        """
        Plot distribution of daily returns
        
        Args:
            stock_data: DataFrame with stock data
            title: Chart title
            save_path: Optional path to save the chart
        """
        returns = stock_data['Close'].pct_change().dropna() * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot histogram
        ax.hist(returns, bins=50, alpha=0.7, color='blue', edgecolor='black')
        
        # Add vertical line at mean
        mean_return = returns.mean()
        ax.axvline(mean_return, color='red', linestyle='--', 
                  linewidth=2, label=f'Mean: {mean_return:.2f}%')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Daily Returns (%)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_correlation_matrix(
        self,
        stocks_data: dict,
        title: str = "Stock Correlation Matrix",
        save_path: Optional[str] = None
    ):
        """
        Plot correlation matrix for multiple stocks
        
        Args:
            stocks_data: Dictionary mapping stock names to their DataFrames
            title: Chart title
            save_path: Optional path to save the chart
        """
        # Create DataFrame with close prices
        price_data = pd.DataFrame()
        for name, data in stocks_data.items():
            if data is not None and 'Close' in data.columns:
                price_data[name] = data['Close']
        
        # Calculate correlation matrix
        correlation = price_data.corr()
        
        # Plot heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1, ax=ax,
                   cbar_kws={"shrink": 0.8})
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_rsi(
        self,
        stock_data: pd.DataFrame,
        rsi_values: pd.Series,
        title: str = "RSI Indicator",
        save_path: Optional[str] = None
    ):
        """
        Plot RSI indicator with overbought/oversold levels
        
        Args:
            stock_data: DataFrame with stock data
            rsi_values: Series with RSI values
            title: Chart title
            save_path: Optional path to save the chart
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                       gridspec_kw={'height_ratios': [2, 1]})
        
        # Plot price
        ax1.plot(stock_data.index, stock_data['Close'], linewidth=2, color='blue')
        ax1.set_ylabel('Price', fontsize=12)
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Plot RSI
        ax2.plot(rsi_values.index, rsi_values, linewidth=2, color='purple')
        ax2.axhline(70, color='red', linestyle='--', linewidth=1, label='Overbought (70)')
        ax2.axhline(30, color='green', linestyle='--', linewidth=1, label='Oversold (30)')
        ax2.fill_between(rsi_values.index, 30, 70, alpha=0.1, color='gray')
        ax2.set_ylabel('RSI', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylim(0, 100)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_comparative_performance(
        self,
        stocks_data: dict,
        title: str = "Comparative Performance",
        normalize: bool = True,
        save_path: Optional[str] = None
    ):
        """
        Plot comparative performance of multiple stocks
        
        Args:
            stocks_data: Dictionary mapping stock names to their DataFrames
            title: Chart title
            normalize: Whether to normalize prices to percentage change
            save_path: Optional path to save the chart
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for name, data in stocks_data.items():
            if data is not None and 'Close' in data.columns:
                prices = data['Close']
                
                if normalize:
                    # Normalize to percentage change from first value
                    normalized = (prices / prices.iloc[0] - 1) * 100
                    ax.plot(data.index, normalized, linewidth=2, label=name)
                else:
                    ax.plot(data.index, prices, linewidth=2, label=name)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Performance (%)' if normalize else 'Price', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        if normalize:
            ax.axhline(0, color='black', linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
