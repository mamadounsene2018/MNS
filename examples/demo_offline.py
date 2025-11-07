"""
Demo script showing the application features without requiring internet access
"""

import sys
sys.path.insert(0, '/home/runner/work/MNS/MNS/src')

from african_stock_analysis import StockDataFetcher
from african_stock_analysis.utils import get_african_exchanges, get_sector_info, format_currency
import pandas as pd
import numpy as np


def demo_offline_features():
    """Demonstrate features that don't require internet access"""
    
    print("=" * 70)
    print("African Stock Market Financial Analysis - Demo")
    print("=" * 70)
    print()
    
    # 1. Show available stocks
    print("1. PRE-CONFIGURED AFRICAN STOCKS")
    print("-" * 70)
    fetcher = StockDataFetcher()
    stocks = fetcher.list_available_stocks()
    
    print(f"Total stocks configured: {len(stocks)}\n")
    for i, (name, symbol) in enumerate(stocks.items(), 1):
        print(f"  {i:2d}. {name:35s} {symbol}")
    print()
    
    # 2. Show African exchanges
    print("2. MAJOR AFRICAN STOCK EXCHANGES")
    print("-" * 70)
    exchanges = get_african_exchanges()
    for code, info in exchanges.items():
        print(f"  {code:10s} - {info['name']}")
        print(f"               Country: {info['country']}, Currency: {info['currency']}, Suffix: {info['suffix']}")
        print()
    
    # 3. Show sectors
    print("3. KEY SECTORS AND MAJOR COMPANIES")
    print("-" * 70)
    sectors = get_sector_info()
    for sector, companies in sectors.items():
        print(f"\n  {sector}:")
        for company in companies:
            print(f"    • {company}")
    print()
    
    # 4. Demonstrate utility functions
    print("4. UTILITY FUNCTIONS")
    print("-" * 70)
    
    # Currency formatting
    print("  Currency Formatting:")
    values = [1234.56, 1500000, 2500000000]
    currencies = ['USD', 'ZAR', 'NGN']
    for val, curr in zip(values, currencies):
        formatted = format_currency(val, curr)
        print(f"    {val:>15,} {curr} → {formatted}")
    print()
    
    # 5. Demonstrate analysis with synthetic data
    print("5. ANALYSIS WITH SAMPLE DATA")
    print("-" * 70)
    
    # Create sample stock data
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    np.random.seed(42)
    
    # Generate realistic price movement
    returns = np.random.normal(0.0005, 0.02, len(dates))
    prices = 100 * np.exp(np.cumsum(returns))
    
    sample_data = pd.DataFrame({
        'Open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
        'High': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
        'Low': prices * (1 - np.random.uniform(0, 0.02, len(dates))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    }, index=dates)
    
    print("  Sample Stock Data (Last 5 Days):")
    print(sample_data.tail().to_string())
    print()
    
    # Calculate some metrics
    total_return = ((sample_data['Close'].iloc[-1] - sample_data['Close'].iloc[0]) / 
                    sample_data['Close'].iloc[0] * 100)
    volatility = sample_data['Close'].pct_change().std() * np.sqrt(252) * 100
    avg_volume = sample_data['Volume'].mean()
    
    print("  Performance Metrics:")
    print(f"    Total Return (6 months): {total_return:+.2f}%")
    print(f"    Annualized Volatility:   {volatility:.2f}%")
    print(f"    Average Daily Volume:    {avg_volume:,.0f}")
    print()
    
    # 6. Show technical analysis capabilities
    print("6. TECHNICAL ANALYSIS CAPABILITIES")
    print("-" * 70)
    print("  Available Indicators:")
    print("    • Simple Moving Average (SMA)")
    print("    • Exponential Moving Average (EMA)")
    print("    • Relative Strength Index (RSI)")
    print("    • MACD (Moving Average Convergence Divergence)")
    print("    • Bollinger Bands")
    print("    • Support and Resistance Levels")
    print("    • Trend Identification")
    print("    • Momentum Score")
    print()
    
    # 7. Show financial ratios available
    print("7. FINANCIAL RATIOS AVAILABLE")
    print("-" * 70)
    print("  Valuation Ratios:")
    print("    • P/E Ratio (Price-to-Earnings)")
    print("    • P/B Ratio (Price-to-Book)")
    print()
    print("  Profitability Ratios:")
    print("    • ROE (Return on Equity)")
    print("    • ROA (Return on Assets)")
    print("    • Profit Margin")
    print()
    print("  Liquidity Ratios:")
    print("    • Current Ratio")
    print("    • Quick Ratio")
    print()
    print("  Leverage Ratios:")
    print("    • Debt-to-Equity Ratio")
    print()
    print("  Growth Metrics:")
    print("    • Earnings Growth")
    print("    • Revenue Growth")
    print("    • Dividend Yield")
    print()
    
    # 8. Show visualization capabilities
    print("8. VISUALIZATION CAPABILITIES")
    print("-" * 70)
    print("  Available Charts:")
    print("    • Price History with Volume")
    print("    • Moving Averages Overlay")
    print("    • Candlestick Charts")
    print("    • Returns Distribution")
    print("    • Correlation Matrix")
    print("    • RSI Indicator")
    print("    • Comparative Performance")
    print()
    
    print("=" * 70)
    print("DEMO COMPLETE!")
    print()
    print("To use with real data, ensure internet connectivity and use:")
    print("  python examples/example_1_basic_analysis.py")
    print("  python examples/example_2_comparative_analysis.py")
    print("  python examples/example_3_market_overview.py")
    print("=" * 70)


if __name__ == "__main__":
    demo_offline_features()
