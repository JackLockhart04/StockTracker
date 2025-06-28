import sys
import os

# Add scripts directory to path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from excel_manager import ExcelManager
from stock_data_handler import StockDataHandler
from api_key_manager import get_stockdata_key

class App:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.excel_manager = ExcelManager(excel_file)
        
    def run(self):
        print(f"Running app with Excel file: {self.excel_file}")
        
        # Check if API key is available
        api_token = get_stockdata_key()
        if api_token:
            print("API key loaded successfully")
        else:
            print("Warning: No API key found. Some features may not work.")
        
        # Print Excel columns
        self.excel_manager.print_excel_columns()
        
        # Update Excel data
        self.excel_manager.update_excel()
