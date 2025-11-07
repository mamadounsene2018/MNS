"""
Example 2: Comparative Analysis of Multiple African Stocks
This example compares multiple stocks across different African countries
"""

import sys
sys.path.insert(0, '/home/runner/work/MNS/MNS/src')

from african_stock_analysis import StockDataFetcher, FinancialRatios, ChartGenerator
import pandas as pd


def main():
    print("=" * 70)
    print("African Stock Analysis - Example 2: Comparative Analysis")
    print("=" * 70)
    print()
    
    # Initialize components
    fetcher = StockDataFetcher()
    
    # Select stocks from different countries for comparison
    comparison_stocks = {
        'MTN Group (SA)': 'MTN.JO',
        'Shoprite (SA)': 'SHP.JO',
        'Standard Bank (SA)': 'SBK.JO',
        'Vodacom (SA)': 'VOD.JO',
    }
    
    print("1. Fetching Data for Multiple Stocks:")
    print("-" * 70)
    
    stocks_data = {}
    stocks_info = {}
    
    for name, symbol in comparison_stocks.items():
        try:
            print(f"  Fetching {name}...", end=" ")
            stocks_data[name] = fetcher.get_stock_data(symbol, period='1y')
            stocks_info[name] = fetcher.get_stock_info(symbol)
            print("✓")
        except Exception as e:
            print(f"✗ ({str(e)})")
            stocks_data[name] = None
            stocks_info[name] = None
    
    print()
    
    # Compare key metrics
    print("2. Key Metrics Comparison:")
    print("-" * 70)
    
    comparison_df = []
    for name, info in stocks_info.items():
        if info:
            ratios = FinancialRatios(info)
            comparison_df.append({
                'Company': name,
                'Current Price': info.get('currentPrice', 'N/A'),
                'P/E Ratio': ratios.get_pe_ratio(),
                'ROE (%)': ratios.get_roe(),
                'Profit Margin (%)': ratios.get_profit_margin(),
                'Market Cap': info.get('marketCap', 'N/A')
            })
    
    if comparison_df:
        df = pd.DataFrame(comparison_df)
        print(df.to_string(index=False))
    print()
    
    # Calculate performance metrics
    print("3. Performance Metrics (1 Year):")
    print("-" * 70)
    
    for name, data in stocks_data.items():
        if data is not None and len(data) > 0:
            first_price = data['Close'].iloc[0]
            last_price = data['Close'].iloc[-1]
            return_pct = ((last_price - first_price) / first_price) * 100
            volatility = data['Close'].pct_change().std() * 100
            
            print(f"{name:25s}: Return: {return_pct:7.2f}% | Volatility: {volatility:.2f}%")
    
    print()
    
    # Volume analysis
    print("4. Average Daily Volume (Last Month):")
    print("-" * 70)
    
    for name, data in stocks_data.items():
        if data is not None and 'Volume' in data.columns and len(data) > 0:
            avg_volume = data['Volume'].tail(30).mean()
            print(f"{name:25s}: {avg_volume:,.0f}")
    
    print()
    
    print("=" * 70)
    print("Comparative Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
