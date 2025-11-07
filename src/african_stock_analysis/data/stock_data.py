"""
Stock data fetcher for African stock exchanges
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class StockDataFetcher:
    """
    Fetches stock data from African exchanges and international sources
    
    Supports major African stock exchanges including:
    - JSE (Johannesburg Stock Exchange) - South Africa
    - NSE (Nairobi Securities Exchange) - Kenya
    - NSE (Nigerian Stock Exchange) - Nigeria
    - BRVM (Bourse Régionale des Valeurs Mobilières) - West Africa
    - CSE (Casablanca Stock Exchange) - Morocco
    - EGX (Egyptian Exchange) - Egypt
    """
    
    # Common African stock symbols and their exchanges
    AFRICAN_STOCKS = {
        # South Africa (JSE)
        'Naspers': 'NPN.JO',
        'MTN Group': 'MTN.JO',
        'Sasol': 'SOL.JO',
        'Standard Bank': 'SBK.JO',
        'Shoprite': 'SHP.JO',
        'Anglo American': 'AGL.JO',
        'FirstRand': 'FSR.JO',
        'Vodacom': 'VOD.JO',
        
        # Nigeria (NSE)
        'Dangote Cement': 'DANGCEM.LG',
        'Guaranty Trust Bank': 'GUARANTY.LG',
        'Zenith Bank': 'ZENITHBANK.LG',
        
        # Kenya (NSE)
        'Safaricom': 'SCOM.NR',
        'Equity Bank': 'EQBNK.NR',
        
        # Egypt (EGX)
        'Commercial International Bank': 'COMI.CA',
        
        # Morocco (CSE)
        'Attijariwafa Bank': 'ATW.CS',
    }
    
    def __init__(self):
        """Initialize the stock data fetcher"""
        self.cache = {}
        
    def get_stock_data(
        self, 
        symbol: str, 
        period: str = '1y',
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        Fetch stock data for a given symbol
        
        Args:
            symbol: Stock ticker symbol (e.g., 'MTN.JO' for MTN Group)
            period: Data period - valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            interval: Data interval - valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            
        Returns:
            DataFrame with stock data (Date, Open, High, Low, Close, Volume, Adj Close)
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
                
            return data
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get detailed information about a stock
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary containing stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info
        except Exception as e:
            raise Exception(f"Error fetching info for {symbol}: {str(e)}")
    
    def get_financial_statements(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """
        Get financial statements for a stock
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with 'income_statement', 'balance_sheet', 'cash_flow'
        """
        try:
            ticker = yf.Ticker(symbol)
            
            statements = {
                'income_statement': ticker.financials,
                'balance_sheet': ticker.balance_sheet,
                'cash_flow': ticker.cashflow
            }
            
            return statements
        except Exception as e:
            raise Exception(f"Error fetching financial statements for {symbol}: {str(e)}")
    
    def get_multiple_stocks(
        self, 
        symbols: List[str], 
        period: str = '1y'
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks
        
        Args:
            symbols: List of stock ticker symbols
            period: Data period
            
        Returns:
            Dictionary mapping symbols to their data DataFrames
        """
        results = {}
        for symbol in symbols:
            try:
                results[symbol] = self.get_stock_data(symbol, period)
            except Exception as e:
                print(f"Warning: Could not fetch data for {symbol}: {str(e)}")
                results[symbol] = None
        
        return results
    
    def get_african_market_overview(self) -> pd.DataFrame:
        """
        Get overview of major African stocks
        
        Returns:
            DataFrame with current prices and basic info for major African stocks
        """
        overview_data = []
        
        for name, symbol in self.AFRICAN_STOCKS.items():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                overview_data.append({
                    'Company': name,
                    'Symbol': symbol,
                    'Current Price': info.get('currentPrice', 'N/A'),
                    'Market Cap': info.get('marketCap', 'N/A'),
                    'Currency': info.get('currency', 'N/A'),
                    'Exchange': info.get('exchange', 'N/A'),
                    'Country': info.get('country', 'N/A')
                })
            except Exception as e:
                print(f"Warning: Could not fetch data for {name} ({symbol}): {str(e)}")
                continue
        
        return pd.DataFrame(overview_data)
    
    @staticmethod
    def list_available_stocks() -> Dict[str, str]:
        """
        List all pre-configured African stocks
        
        Returns:
            Dictionary mapping company names to ticker symbols
        """
        return StockDataFetcher.AFRICAN_STOCKS.copy()
