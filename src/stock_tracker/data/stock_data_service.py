"""
Stock Data Service Module

This module provides services for fetching and processing stock market data
from various API providers including StockData.org and Alpha Vantage.
"""

import json
import logging
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Any
from ..config.api_key_manager import get_stockdata_key

# Configure logging for this module
logger = logging.getLogger(__name__)


class StockDataService:
    """
    Service class for handling stock market data operations.
    
    This class provides methods to fetch stock data from various APIs,
    parse the responses, and format the data for use in the application.
    """
    
    # API endpoints
    STOCKDATA_ORG_BASE_URL = "https://api.stockdata.org/v1/data/eod"
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    
    @staticmethod
    def print_stock_prices(prices: Dict[str, Dict[str, Any]]) -> None:
        """
        Print formatted stock price data for each date.
        
        Args:
            prices: Dictionary of prices from parse_stock_data
        """
        if not prices:
            print("No price data available")
            return
        
        print("Stock Price Data:")
        print("-" * 50)
        
        # Sort dates for chronological order
        sorted_dates = sorted(prices.keys())
        
        for date in sorted_dates:
            data = prices[date]
            print(f"Date: {date}")
            print(f"  Open:  ${data['open']:.2f}")
            print(f"  Close: ${data['close']:.2f}")
            print(f"  High:  ${data['high']:.2f}")
            print(f"  Low:   ${data['low']:.2f}")
            print(f"  Volume: {data['volume']:,}")
            print()
    
    @classmethod
    def get_stock_data_from_api(cls, symbol: str, date_from: str, date_to: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Get stock data from the primary API source.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format (optional)
            
        Returns:
            Dictionary containing stock data organized by date
        """
        logger.info(f"Fetching stock data for symbol: {symbol} from {date_from} to {date_to or 'latest'}")
        return cls.get_stock_data_from_stockdata_org(symbol, date_from, date_to)
    
    @staticmethod
    def parse_stockdata_org_response(json_response: Any) -> Dict[str, Dict[str, Any]]:
        """
        Parse stock data from StockData.org API response.
        
        Args:
            json_response: JSON response from the API
            
        Returns:
            Dictionary with dates as keys and price data as values
        """
        try:
            # Parse JSON if it's a string
            if isinstance(json_response, str):
                data = json.loads(json_response)
            else:
                data = json_response
            
            # Handle different response formats
            if isinstance(data, dict):
                # Check if it's the format with 'data' array
                if 'data' in data:
                    stock_data = data.get('data', [])
                else:
                    # Direct format where the dict contains date keys
                    return data
            else:
                # If it's already a list
                stock_data = data
            
            # Create dictionary to store price data
            prices = {}
            
            for entry in stock_data:
                # Extract date and convert to readable format
                date_str = entry.get('date', '')
                if date_str:
                    # Parse the ISO date string
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    # Convert to local date string (YYYY-MM-DD)
                    date_key = date_obj.strftime('%Y-%m-%d')
                    
                    # Extract price data
                    prices[date_key] = {
                        'open': entry.get('open'),
                        'close': entry.get('close'),
                        'high': entry.get('high'),
                        'low': entry.get('low'),
                        'volume': entry.get('volume')
                    }
            
            logger.info(f"Successfully parsed {len(prices)} data points from API response")
            return prices
            
        except Exception as error:
            logger.error(f"Error parsing stock data: {error}")
            return {}
    
    @classmethod
    def get_stock_data_from_stockdata_org(cls, symbol: str, date_from: str, date_to: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Fetch stock data from StockData.org API.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format (optional)
            
        Returns:
            Dictionary containing stock data organized by date
        """
        # Get API key from manager
        api_token = get_stockdata_key()
        
        if not api_token:
            logger.error("API token not found. Check your api_credentials/keys.txt file.")
            print("Error: API token not found. Check your api_credentials/keys.txt file.")
            return {}
        
        # Build API URL
        url = f"{cls.STOCKDATA_ORG_BASE_URL}?symbols={symbol}&date_from={date_from}"
        if date_to:
            url += f"&date_to={date_to}"
        url += f"&api_token={api_token}"
        
        # Log the API call URL (without the token for security)
        safe_url = f"{cls.STOCKDATA_ORG_BASE_URL}?symbols={symbol}&date_from={date_from}"
        if date_to:
            safe_url += f"&date_to={date_to}"
        safe_url += "&api_token=[HIDDEN]"
        logger.info(f"Making API call to StockData.org: {safe_url}")
        
        try:
            logger.info(f"Fetching data for {symbol} from {date_from} to {date_to or 'latest'}")
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Log response status and size
            logger.info(f"API response received - Status: {response.status_code}, Size: {len(response.content)} bytes")
            
            # Parse the response
            response_json = cls.parse_stockdata_org_response(response.json())
            
            # Log the parsed data summary
            if response_json:
                dates = sorted(response_json.keys())
                logger.info(f"Stock data summary for {symbol}: {len(dates)} days from {dates[0]} to {dates[-1]}")
                logger.debug(f"Stock data for {symbol}: {json.dumps(response_json, indent=2)}")
            else:
                logger.warning(f"No stock data received for {symbol}")
            
            return response_json
            
        except requests.exceptions.RequestException as error:
            logger.error(f"Error fetching data from API for {symbol}: {error}")
            print(f"Error fetching data from API: {error}")
            return {}
        except Exception as error:
            logger.error(f"Error processing API response for {symbol}: {error}")
            print(f"Error processing API response: {error}")
            return {}
    
    @staticmethod
    def parse_alphavantage_response(json_response: Any) -> Dict[str, Dict[str, Any]]:
        """
        Parse stock data from Alpha Vantage API response.
        
        Args:
            json_response: JSON response from the API
            
        Returns:
            Dictionary with dates as keys and price data as values
        """
        logger.info(f"Parsing Alpha Vantage data of type {type(json_response)}")
        # TODO: Implement Alpha Vantage parsing logic
        return {}
    
    @classmethod
    def get_stock_data_from_alphavantage(cls, symbol: str, date_from: str, date_to: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Fetch stock data from Alpha Vantage API.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format (optional)
            
        Returns:
            Dictionary containing stock data organized by date
        """
        # Get API key from manager
        api_token = get_stockdata_key()
        
        if not api_token:
            logger.error("API token not found. Check your api_credentials/keys.txt file.")
            print("Error: API token not found. Check your api_credentials/keys.txt file.")
            return {}
        
        # Build API URL
        url = f"{cls.ALPHA_VANTAGE_BASE_URL}?function=TIME_SERIES_DAILY"
        url += f"&symbol={symbol}"
        url += f"&outputsize=compact"
        url += f"&apikey={api_token}"
        
        # Log the API call URL (without the token for security)
        safe_url = f"{cls.ALPHA_VANTAGE_BASE_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey=[HIDDEN]"
        logger.info(f"Making API call to Alpha Vantage: {safe_url}")
        
        try:
            logger.info(f"Fetching Alpha Vantage data for {symbol}")
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Log response status and size
            logger.info(f"Alpha Vantage API response received - Status: {response.status_code}, Size: {len(response.content)} bytes")
            
            # Parse the response
            return cls.parse_alphavantage_response(response.json())
            
        except requests.exceptions.RequestException as error:
            logger.error(f"Error fetching data from Alpha Vantage API for {symbol}: {error}")
            print(f"Error fetching data from API: {error}")
            return {}


# Example usage
if __name__ == "__main__":
    # Example with sample data
    sample_stock_data = {
        "2025-06-20": {"open": 700.55, "close": 682.59, "high": 701.7, "low": 678.84, "volume": 357997},
        "2025-06-18": {"open": 697.99, "close": 695.63, "high": 701.59, "low": 694.99, "volume": 209316},
        "2025-06-17": {"open": 701.74, "close": 697.37, "high": 705.9, "low": 696.16, "volume": 216896},
        "2025-06-16": {"open": 699.33, "close": 702.07, "high": 707.14, "low": 693.55, "volume": 345675}
    }
    
    # Print the sample data
    StockDataService.print_stock_prices(sample_stock_data)
    
    # Example API call (uncomment when ready to test)
    # stock_symbol = 'META'
    # stock_data = StockDataService.get_stock_data_from_api(stock_symbol, '2025-06-15', '2025-06-23')
    # StockDataService.print_stock_prices(stock_data) 