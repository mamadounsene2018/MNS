"""
Utility functions for the African Stock Analysis package
"""
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta


def format_currency(value: float, currency: str = 'USD') -> str:
    """
    Format currency values
    
    Args:
        value: Numeric value
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    if pd.isna(value) or value is None:
        return 'N/A'
    
    symbols = {
        'USD': '$',
        'ZAR': 'R',
        'NGN': '₦',
        'KES': 'KSh',
        'EGP': 'E£',
        'MAD': 'DH',
    }
    
    symbol = symbols.get(currency, currency + ' ')
    
    if abs(value) >= 1e9:
        return f"{symbol}{value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"{symbol}{value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"{symbol}{value/1e3:.2f}K"
    else:
        return f"{symbol}{value:.2f}"


def calculate_returns(prices: pd.Series, period: str = 'daily') -> pd.Series:
    """
    Calculate returns for different periods
    
    Args:
        prices: Series of prices
        period: Period type ('daily', 'weekly', 'monthly')
        
    Returns:
        Series of returns
    """
    periods = {
        'daily': 1,
        'weekly': 5,
        'monthly': 21
    }
    
    return prices.pct_change(periods=periods.get(period, 1))


def get_african_exchanges() -> Dict[str, Dict[str, str]]:
    """
    Get information about major African stock exchanges
    
    Returns:
        Dictionary with exchange information
    """
    return {
        'JSE': {
            'name': 'Johannesburg Stock Exchange',
            'country': 'South Africa',
            'currency': 'ZAR',
            'suffix': '.JO'
        },
        'NSE_NG': {
            'name': 'Nigerian Stock Exchange',
            'country': 'Nigeria',
            'currency': 'NGN',
            'suffix': '.LG'
        },
        'NSE_KE': {
            'name': 'Nairobi Securities Exchange',
            'country': 'Kenya',
            'currency': 'KES',
            'suffix': '.NR'
        },
        'EGX': {
            'name': 'Egyptian Exchange',
            'country': 'Egypt',
            'currency': 'EGP',
            'suffix': '.CA'
        },
        'BRVM': {
            'name': 'Bourse Régionale des Valeurs Mobilières',
            'country': 'West Africa',
            'currency': 'XOF',
            'suffix': '.BR'
        },
        'CSE': {
            'name': 'Casablanca Stock Exchange',
            'country': 'Morocco',
            'currency': 'MAD',
            'suffix': '.CS'
        }
    }


def get_sector_info() -> Dict[str, List[str]]:
    """
    Get common African stock sectors
    
    Returns:
        Dictionary mapping sectors to example companies
    """
    return {
        'Banking & Finance': [
            'Standard Bank', 'FirstRand', 'Guaranty Trust Bank', 
            'Zenith Bank', 'Equity Bank', 'Attijariwafa Bank'
        ],
        'Telecommunications': [
            'MTN Group', 'Vodacom', 'Safaricom'
        ],
        'Mining & Resources': [
            'Anglo American', 'Sasol'
        ],
        'Consumer Goods': [
            'Shoprite', 'Dangote Cement', 'Naspers'
        ]
    }


def filter_by_date_range(
    data: pd.DataFrame,
    start_date: str = None,
    end_date: str = None
) -> pd.DataFrame:
    """
    Filter DataFrame by date range
    
    Args:
        data: DataFrame with datetime index
        start_date: Start date (ISO format)
        end_date: End date (ISO format)
        
    Returns:
        Filtered DataFrame
    """
    filtered = data.copy()
    
    if start_date:
        filtered = filtered[filtered.index >= pd.to_datetime(start_date)]
    
    if end_date:
        filtered = filtered[filtered.index <= pd.to_datetime(end_date)]
    
    return filtered


def generate_report_date() -> str:
    """
    Generate formatted date for reports
    
    Returns:
        Formatted date string
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
