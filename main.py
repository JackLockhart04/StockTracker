import sys
import os

# Add scripts directory to path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Use the ExcelReader class to read the Excel file
from app import App

def main():
    excel_file = "chatGptStocks.xlsx"
    
    app = App(excel_file)
    app.run()

if __name__ == "__main__":
    main()
