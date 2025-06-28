import json
import requests
from datetime import datetime, timezone, timedelta

class StockDataHandler:
    _api_token = None
    _StockDataOrg_base_url = "https://api.stockdata.org/v1/data/eod"
    _AlphaVantage_base_url = "https://www.alphavantage.co/query"
    
    @classmethod
    def set_api_token(cls, api_token):
        """Set the API token globally"""
        cls._api_token = api_token
    
    @classmethod
    def get_api_token(cls):
        """Get the current API token"""
        return cls._api_token
    
    @staticmethod
    def print_open_close_prices(prices):
        """
        Print open and close prices for each date
        
        Args:
            prices (dict): Dictionary of prices from parse_stock_data
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
    def get_stock_data_from_api(cls, symbol, date_from, date_to=None):
        return cls.get_stock_data_from_StockDataOrg(symbol, date_from, date_to)
    

    @staticmethod
    def parse_StockDataOrg_data(json_response):
        """
        Parse stock data from API response and extract open/close prices
        
        Args:
            json_response (str or dict): JSON response from the API
            
        Returns:
            dict: Dictionary with dates as keys and (open, close) as values
        """
        # print(f"Parsing stock data of type {type(json_response)}")
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
            
            # Create dictionary to store open/close prices
            prices = {}
            
            for entry in stock_data:
                # Extract date and convert to readable format
                date_str = entry.get('date', '')
                if date_str:
                    # Parse the ISO date string
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    # Convert to local date string (YYYY-MM-DD)
                    date_key = date_obj.strftime('%Y-%m-%d')
                    
                    # Extract open and close prices
                    open_price = entry.get('open')
                    close_price = entry.get('close')
                    
                    # Store in dictionary
                    prices[date_key] = {
                        'open': open_price,
                        'close': close_price,
                        'high': entry.get('high'),
                        'low': entry.get('low'),
                        'volume': entry.get('volume')
                    }
            
            return prices
            
        except Exception as e:
            print(f"Error parsing stock data: {e}")
            return {}

    @classmethod
    def get_stock_data_from_StockDataOrg(cls, symbol, date_from, date_to=None):
        if not cls._api_token:
            print("Error: API token not provided. Use StockDataHandler.set_api_token() first.")
            return {}
        
        # Build API URL
        url = f"{cls._StockDataOrg_base_url}?symbols={symbol}&date_from={date_from}"
        if date_to:
            url += f"&date_to={date_to}"
        url += f"&api_token={cls._api_token}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse the response
            response_json = cls.parse_StockDataOrg_data(response.json())
            return response_json
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return {}
        except Exception as e:
            print(f"Error processing API response: {e}")
            return {}
    

    @staticmethod
    def parse_AlphaVantage_data(json_response):
        """
        Parse stock data from API response and extract open/close prices
        
        Args:
            json_response (str or dict): JSON response from the API
        """
        print(f"Parsing stock data of type {type(json_response)}")
       
    @classmethod
    def get_stock_data_from_AlphaVantage(cls, symbol, date_from, date_to=None):
        if not cls._api_token:
            print("Error: API token not provided. Use StockDataHandler.set_api_token() first.")
            return {}
        
        # Build API URL
        url = f"{cls._AlphaVantage_base_url}?function=TIME_SERIES_DAILY"
        url += f"&symbol={symbol}"
        url += f"&outputsize=compact"
        url += f"&apikey={cls._api_token}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse the response
            return cls.parse_AlphaVantage_data(response.json())
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")

# Example usage
if __name__ == "__main__":
    # Example with the provided JSON data
    stock_data = '''{"2025-06-20": {"open": 700.55, "close": 682.59, "high": 701.7, "low": 678.84, "volume": 357997}, "2025-06-18": {"open": 697.99, "close": 695.63, "high": 701.59, "low": 694.99, "volume": 209316}, "2025-06-17": {"open": 701.74, "close": 697.37, "high": 705.9, "low": 696.16, "volume": 216896}, "2025-06-16": {"open": 699.33, "close": 702.07, "high": 707.14, "low": 693.55, "volume": 345675}}'''
    stock_data = json.loads(stock_data)
    print(type(stock_data))
    
    handler = StockDataHandler(api_token='13kRSGqjRZMYdj77eoAqhfDv5UXOHC9igGaOreb0')
    stock_symbol = 'META'
    # stock_data = handler.get_stock_data_from_api(stock_symbol, '2025-06-15', '2025-06-23')
    prices = handler.parse_StockDataOrg_data(stock_data)
    handler.print_open_close_prices(prices) 