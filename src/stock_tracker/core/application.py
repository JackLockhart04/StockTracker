"""
Stock Tracker Application Module

This module contains the main application class that orchestrates the stock tracking
functionality, including Excel file management and API integration.
"""

from typing import Optional
from ..data.excel_service import ExcelService
from ..data.stock_data_service import StockDataService
from ..config.api_key_manager import get_stockdata_key


class StockTrackerApplication:
    """
    Main application class for the stock tracking system.
    
    This class orchestrates the interaction between Excel file management,
    stock data services, and API key management to provide a complete
    stock tracking solution.
    """
    
    def __init__(self, excel_file_path: str):
        """
        Initialize the stock tracker application.
        
        Args:
            excel_file_path: Path to the Excel file for stock tracking
        """
        self.excel_file_path = excel_file_path
        self.excel_service = ExcelService(excel_file_path)
        
    def run(self) -> None:
        """
        Run the main application workflow.
        
        This method executes the complete stock tracking process:
        1. Validates API key availability
        2. Displays Excel file structure
        3. Updates stock data in the Excel file
        """
        print(f"Running Stock Tracker Application with Excel file: {self.excel_file_path}")
        print("=" * 60)
        
        # Check if API key is available
        self._validate_api_key()
        
        # Display Excel file information
        self._display_excel_info()
        
        # Update Excel data
        self._update_stock_data()
        
        print("=" * 60)
        print("Stock Tracker Application completed successfully!")
    
    def _validate_api_key(self) -> None:
        """
        Validate that the required API key is available.
        
        Checks for the StockData.org API key and provides appropriate
        feedback to the user.
        """
        api_token = get_stockdata_key()
        if api_token:
            print("✓ API key loaded successfully")
        else:
            print("⚠ Warning: No API key found. Some features may not work.")
            print("  Please check your api_credentials/keys.txt file.")
    
    def _display_excel_info(self) -> None:
        """
        Display information about the Excel file structure.
        
        Shows the column names and structure of the Excel file
        to help users understand the data format.
        """
        print("\nExcel File Structure:")
        print("-" * 30)
        self.excel_service.print_excel_columns()
    
    def _update_stock_data(self) -> None:
        """
        Update the Excel file with current stock data.
        
        Fetches the latest stock data for all symbols in the Excel file
        and updates the file with current prices and performance metrics.
        """
        print("\nUpdating Stock Data:")
        print("-" * 30)
        self.excel_service.update_excel()
    
    def create_new_excel_file(self) -> None:
        """
        Create a new Excel file with the proper structure.
        
        Creates a new Excel file with all the required columns for
        stock tracking, including proper formatting and headers.
        """
        print(f"Creating new Excel file: {self.excel_file_path}")
        self.excel_service.create_excel()
    
    def get_stock_data_for_symbol(self, symbol: str, date_from: str, date_to: Optional[str] = None) -> dict:
        """
        Get stock data for a specific symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format (optional)
            
        Returns:
            Dictionary containing stock data for the specified symbol
        """
        return StockDataService.get_stock_data_from_api(symbol, date_from, date_to)
    
    def print_stock_data(self, stock_data: dict) -> None:
        """
        Print formatted stock data.
        
        Args:
            stock_data: Dictionary containing stock data to display
        """
        StockDataService.print_stock_prices(stock_data)


# Example usage
if __name__ == "__main__":
    # Example usage of the application
    excel_file = "stock_tracking.xlsx"
    app = StockTrackerApplication(excel_file)
    
    # Create a new Excel file (uncomment if needed)
    # app.create_new_excel_file()
    
    # Run the main application
    app.run()
    
    # Example of getting data for a specific symbol
    # symbol = "AAPL"
    # stock_data = app.get_stock_data_for_symbol(symbol, "2025-01-01", "2025-01-07")
    # app.print_stock_data(stock_data) 