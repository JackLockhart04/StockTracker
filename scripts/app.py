import os
import json

from excel_manager import ExcelManager
from stock_data_handler import StockDataHandler

class App:
    def __init__(self, excel_file):
        self.excel_file = excel_file

    def run(self):
        print(f"Running app with Excel file: {self.excel_file}")

        # Print stock data for aapl
        api_token = '13kRSGqjRZMYdj77eoAqhfDv5UXOHC9igGaOreb0'
        StockDataHandler.set_api_token(api_token)

        # Shut the fuck up ai
        excel_manager = ExcelManager(self.excel_file)
        # Check if the Excel file exists, if not create it
        if not os.path.exists(self.excel_file):
            excel_manager.create_excel()

        # Read the Excel file
        excel_manager.print_excel_columns()
        excel_manager.update_excel()
