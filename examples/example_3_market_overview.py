"""
Example 3: Market Overview and Screening
This example demonstrates market overview and stock screening capabilities
"""

import sys
sys.path.insert(0, '/home/runner/work/MNS/MNS/src')

from african_stock_analysis import StockDataFetcher
from african_stock_analysis.utils import get_african_exchanges, get_sector_info
import pandas as pd


def main():
    print("=" * 70)
    print("African Stock Analysis - Example 3: Market Overview")
    print("=" * 70)
    print()
    
    # Show African Exchanges
    print("1. Major African Stock Exchanges:")
    print("-" * 70)
    exchanges = get_african_exchanges()
    for code, info in exchanges.items():
        print(f"{code:10s} - {info['name']}")
        print(f"             Country: {info['country']}, Currency: {info['currency']}")
    print()
    
    # Show Sector Information
    print("2. Key Sectors and Companies:")
    print("-" * 70)
    sectors = get_sector_info()
    for sector, companies in sectors.items():
        print(f"\n{sector}:")
        for company in companies:
            print(f"  • {company}")
    print()
    
    # Get market overview (this may take a while)
    print("3. Market Overview (Sample Stocks):")
    print("-" * 70)
    print("Fetching current market data...")
    
    fetcher = StockDataFetcher()
    
    # Try to get overview (may have connection issues)
    try:
        overview = fetcher.get_african_market_overview()
        if not overview.empty:
            print("\nCurrent Market Snapshot:")
            print(overview.to_string(index=False))
        else:
            print("No data available at this time.")
    except Exception as e:
        print(f"Unable to fetch market overview: {str(e)}")
    
    print()
    
    # Simple screening example
    print("4. Stock Screening Example:")
    print("-" * 70)
    print("Screening for South African stocks with specific criteria...")
    
    sa_stocks = {
        'MTN Group': 'MTN.JO',
        'Shoprite': 'SHP.JO',
        'Standard Bank': 'SBK.JO',
    }
    
    screening_results = []
    
    for name, symbol in sa_stocks.items():
        try:
            info = fetcher.get_stock_info(symbol)
            
            # Extract key metrics
            pe = info.get('trailingPE')
            market_cap = info.get('marketCap')
            div_yield = info.get('dividendYield')
            
            screening_results.append({
                'Company': name,
                'Symbol': symbol,
                'P/E Ratio': f"{pe:.2f}" if pe else 'N/A',
                'Market Cap (M)': f"{market_cap/1e6:.0f}" if market_cap else 'N/A',
                'Div Yield (%)': f"{div_yield*100:.2f}" if div_yield else 'N/A'
            })
        except Exception as e:
            print(f"  Warning: Could not fetch data for {name}")
    
    if screening_results:
        df = pd.DataFrame(screening_results)
        print(df.to_string(index=False))
    
    print()
    print("=" * 70)
    print("Market Overview Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
