"""
Financial ratios calculator for stock analysis
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


class FinancialRatios:
    """
    Calculate various financial ratios for stock analysis
    
    Includes:
    - Profitability ratios (ROE, ROA, Profit Margin, etc.)
    - Liquidity ratios (Current Ratio, Quick Ratio)
    - Leverage ratios (Debt-to-Equity, Interest Coverage)
    - Efficiency ratios (Asset Turnover, Inventory Turnover)
    - Valuation ratios (P/E, P/B, EV/EBITDA)
    """
    
    def __init__(self, stock_info: Dict, financial_statements: Optional[Dict] = None):
        """
        Initialize with stock information and financial statements
        
        Args:
            stock_info: Dictionary containing stock information
            financial_statements: Dictionary with income statement, balance sheet, cash flow
        """
        self.info = stock_info
        self.statements = financial_statements or {}
    
    def get_pe_ratio(self) -> Optional[float]:
        """
        Calculate Price-to-Earnings ratio
        
        Returns:
            P/E ratio or None if not available
        """
        return self.info.get('trailingPE') or self.info.get('forwardPE')
    
    def get_pb_ratio(self) -> Optional[float]:
        """
        Calculate Price-to-Book ratio
        
        Returns:
            P/B ratio or None if not available
        """
        return self.info.get('priceToBook')
    
    def get_roe(self) -> Optional[float]:
        """
        Calculate Return on Equity
        
        Returns:
            ROE as a percentage or None if not available
        """
        roe = self.info.get('returnOnEquity')
        if roe is not None:
            return roe * 100  # Convert to percentage
        return None
    
    def get_roa(self) -> Optional[float]:
        """
        Calculate Return on Assets
        
        Returns:
            ROA as a percentage or None if not available
        """
        roa = self.info.get('returnOnAssets')
        if roa is not None:
            return roa * 100  # Convert to percentage
        return None
    
    def get_profit_margin(self) -> Optional[float]:
        """
        Calculate Profit Margin
        
        Returns:
            Profit margin as a percentage or None if not available
        """
        margin = self.info.get('profitMargins')
        if margin is not None:
            return margin * 100  # Convert to percentage
        return None
    
    def get_current_ratio(self) -> Optional[float]:
        """
        Calculate Current Ratio (Current Assets / Current Liabilities)
        
        Returns:
            Current ratio or None if not available
        """
        return self.info.get('currentRatio')
    
    def get_quick_ratio(self) -> Optional[float]:
        """
        Calculate Quick Ratio
        
        Returns:
            Quick ratio or None if not available
        """
        return self.info.get('quickRatio')
    
    def get_debt_to_equity(self) -> Optional[float]:
        """
        Calculate Debt-to-Equity ratio
        
        Returns:
            D/E ratio or None if not available
        """
        return self.info.get('debtToEquity')
    
    def get_earnings_growth(self) -> Optional[float]:
        """
        Get earnings growth rate
        
        Returns:
            Earnings growth as a percentage or None if not available
        """
        growth = self.info.get('earningsGrowth')
        if growth is not None:
            return growth * 100  # Convert to percentage
        return None
    
    def get_revenue_growth(self) -> Optional[float]:
        """
        Get revenue growth rate
        
        Returns:
            Revenue growth as a percentage or None if not available
        """
        growth = self.info.get('revenueGrowth')
        if growth is not None:
            return growth * 100  # Convert to percentage
        return None
    
    def get_dividend_yield(self) -> Optional[float]:
        """
        Get dividend yield
        
        Returns:
            Dividend yield as a percentage or None if not available
        """
        div_yield = self.info.get('dividendYield')
        if div_yield is not None:
            return div_yield * 100  # Convert to percentage
        return None
    
    def get_beta(self) -> Optional[float]:
        """
        Get stock beta (volatility relative to market)
        
        Returns:
            Beta value or None if not available
        """
        return self.info.get('beta')
    
    def get_all_ratios(self) -> Dict[str, Optional[float]]:
        """
        Get all available financial ratios
        
        Returns:
            Dictionary with all calculated ratios
        """
        return {
            'P/E Ratio': self.get_pe_ratio(),
            'P/B Ratio': self.get_pb_ratio(),
            'ROE (%)': self.get_roe(),
            'ROA (%)': self.get_roa(),
            'Profit Margin (%)': self.get_profit_margin(),
            'Current Ratio': self.get_current_ratio(),
            'Quick Ratio': self.get_quick_ratio(),
            'Debt-to-Equity': self.get_debt_to_equity(),
            'Earnings Growth (%)': self.get_earnings_growth(),
            'Revenue Growth (%)': self.get_revenue_growth(),
            'Dividend Yield (%)': self.get_dividend_yield(),
            'Beta': self.get_beta(),
        }
    
    def get_valuation_summary(self) -> str:
        """
        Get a text summary of valuation metrics
        
        Returns:
            Formatted string with valuation summary
        """
        ratios = self.get_all_ratios()
        
        summary = "=== Valuation Metrics ===\n"
        for metric, value in ratios.items():
            if value is not None:
                summary += f"{metric}: {value:.2f}\n"
            else:
                summary += f"{metric}: N/A\n"
        
        return summary
    
    @staticmethod
    def calculate_price_returns(prices: pd.Series, periods: int = 1) -> pd.Series:
        """
        Calculate price returns
        
        Args:
            prices: Series of prices
            periods: Number of periods for return calculation
            
        Returns:
            Series of returns
        """
        return prices.pct_change(periods=periods) * 100
    
    @staticmethod
    def calculate_volatility(returns: pd.Series, annualize: bool = True) -> float:
        """
        Calculate volatility (standard deviation of returns)
        
        Args:
            returns: Series of returns
            annualize: Whether to annualize the volatility
            
        Returns:
            Volatility value
        """
        vol = returns.std()
        if annualize:
            # Assuming daily returns, annualize with sqrt(252) trading days
            vol = vol * np.sqrt(252)
        return vol
