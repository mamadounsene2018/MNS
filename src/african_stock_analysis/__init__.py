"""
African Stock Analysis - A comprehensive financial analysis toolkit for African stock markets
"""

__version__ = "1.0.0"
__author__ = "MNS"

from .data.stock_data import StockDataFetcher
from .analysis.financial_ratios import FinancialRatios
from .analysis.trend_analysis import TrendAnalyzer
from .visualization.charts import ChartGenerator

__all__ = [
    'StockDataFetcher',
    'FinancialRatios',
    'TrendAnalyzer',
    'ChartGenerator',
]
