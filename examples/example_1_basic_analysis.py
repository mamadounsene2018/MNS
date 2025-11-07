"""
Example 1: Basic Stock Data Fetching and Analysis
This example demonstrates how to fetch and analyze stock data for African companies
"""

import sys
sys.path.insert(0, '/home/runner/work/MNS/MNS/src')

from african_stock_analysis import StockDataFetcher, FinancialRatios, TrendAnalyzer, ChartGenerator


def main():
    print("=" * 70)
    print("African Stock Analysis - Example 1: Basic Analysis")
    print("=" * 70)
    print()
    
    # Initialize the stock data fetcher
    fetcher = StockDataFetcher()
    
    # Example 1: Get list of available stocks
    print("1. Available African Stocks:")
    print("-" * 70)
    stocks = fetcher.list_available_stocks()
    for i, (name, symbol) in enumerate(stocks.items(), 1):
        print(f"{i:2d}. {name:30s} - {symbol}")
    print()
    
    # Example 2: Fetch data for a specific stock (MTN Group)
    print("2. Fetching Data for MTN Group (South Africa):")
    print("-" * 70)
    try:
        symbol = 'MTN.JO'
        stock_data = fetcher.get_stock_data(symbol, period='6mo')
        print(f"✓ Successfully fetched {len(stock_data)} days of data")
        print(f"  Date Range: {stock_data.index[0].date()} to {stock_data.index[-1].date()}")
        print(f"  Latest Close Price: {stock_data['Close'].iloc[-1]:.2f}")
        print()
        
        # Example 3: Get stock information
        print("3. Stock Information:")
        print("-" * 70)
        info = fetcher.get_stock_info(symbol)
        print(f"  Company: {info.get('longName', 'N/A')}")
        print(f"  Sector: {info.get('sector', 'N/A')}")
        print(f"  Industry: {info.get('industry', 'N/A')}")
        print(f"  Market Cap: {info.get('marketCap', 'N/A'):,}")
        print(f"  Currency: {info.get('currency', 'N/A')}")
        print()
        
        # Example 4: Calculate Financial Ratios
        print("4. Financial Ratios Analysis:")
        print("-" * 70)
        ratios = FinancialRatios(info)
        print(ratios.get_valuation_summary())
        
        # Example 5: Technical Analysis
        print("5. Technical Analysis:")
        print("-" * 70)
        analyzer = TrendAnalyzer(stock_data)
        print(analyzer.get_analysis_summary())
        
        # Example 6: Generate Charts (commented out as they require display)
        # print("6. Generating Charts...")
        # print("-" * 70)
        # chart_gen = ChartGenerator()
        # chart_gen.plot_price_history(stock_data, title=f"{info.get('longName', symbol)} - Price History")
        # chart_gen.plot_moving_averages(stock_data, periods=[20, 50])
        # print("✓ Charts generated successfully")
        # print()
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print()
    
    print("=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
