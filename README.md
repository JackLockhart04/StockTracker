# Stock Tracker Application

A comprehensive Python application for tracking stock performance using Excel files and real-time market data APIs.

## 🚀 Features

- **Excel Integration**: Create and manage Excel files for stock tracking
- **Real-time Data**: Fetch current stock prices from StockData.org API
- **Performance Tracking**: Track 7-day stock performance with daily price changes
- **Automated Updates**: Bulk update stock data for multiple symbols
- **Professional Formatting**: Excel files with proper formatting and styling

## 📁 Project Structure

```
stocks/
├── src/
│   ├── stock_tracker/
│   │   ├── core/
│   │   │   └── application_new.py          # Main application logic
│   │   ├── data/
│   │   │   ├── stock_data_service_new.py   # Stock data API integration
│   │   │   └── excel_service_new.py        # Excel file management
│   │   ├── config/
│   │   │   └── api_key_manager_new.py      # API key management
│   │   └── __init__.py
│   ├── main_new.py                         # Application entry point
│   └── __init__.py
├── tests/                                  # Test files (future)
├── docs/                                   # Documentation (future)
├── venv/                                   # Virtual environment
├── .gitignore                              # Git ignore rules
├── .cursorignore                           # Cursor AI ignore rules
└── README_new.md                           # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd stocks
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install pandas openpyxl requests
   ```

4. **Configure API Keys**
   - Navigate to `src/stock_tracker/config/api_credentials/`
   - Edit `keys.txt` with your API keys:
     ```
     'StockData.org': YOUR_STOCKDATA_API_KEY
     'Alpha Vantage': YOUR_ALPHAVANTAGE_API_KEY
     'Finnhub': YOUR_FINNHUB_API_KEY
     ```

## 🚀 Usage

### Basic Usage

1. **Run the application**
   ```bash
   python src/main_new.py
   ```

2. **Create a new Excel file**
   ```python
   from src.stock_tracker.core.application_new import StockTrackerApplication
   
   app = StockTrackerApplication("my_stocks.xlsx")
   app.create_new_excel_file()
   ```

3. **Get stock data for a specific symbol**
   ```python
   from src.stock_tracker.data.stock_data_service_new import StockDataService
   
   # Get data for AAPL from Jan 1-7, 2025
   stock_data = StockDataService.get_stock_data_from_api("AAPL", "2025-01-01", "2025-01-07")
   StockDataService.print_stock_prices(stock_data)
   ```

### Excel File Structure

The application creates Excel files with the following columns:

| Column | Description |
|--------|-------------|
| Symbol | Stock symbol (e.g., AAPL, MSFT) |
| Purchase Date | Date you started tracking |
| Initial Price | Price when tracking began |
| End Price | Final price after 7 days |
| Total Change Pct | Total percentage change over the week |
| Day 1-7 Price | Daily closing prices |
| Day 1-7 Change Pct | Daily percentage changes from initial price |

## 🔧 Configuration

### API Keys

The application supports multiple stock data providers:

- **StockData.org** (Primary): Real-time stock data
- **Alpha Vantage**: Alternative data source
- **Finnhub**: Additional market data

### File Paths

- **Excel Files**: Located in the project root directory
- **API Credentials**: `src/stock_tracker/config/api_credentials/keys.txt`
- **Logs**: Console output (can be extended to file logging)

## 🧪 Development

### Code Organization

The application follows a modular architecture:

- **Core**: Main application logic and orchestration
- **Data**: Data services for API integration and Excel management
- **Config**: Configuration management and API key handling

### Naming Conventions

- **Classes**: PascalCase (e.g., `StockDataService`)
- **Functions/Methods**: snake_case (e.g., `get_stock_data`)
- **Variables**: snake_case (e.g., `file_path`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `STOCKDATA_ORG_BASE_URL`)

### Adding New Features

1. **New API Provider**: Add methods to `StockDataService`
2. **New Excel Features**: Extend `ExcelService`
3. **Configuration**: Update `ApiKeyManager`

## 📝 API Documentation

### StockDataService

```python
class StockDataService:
    @classmethod
    def get_stock_data_from_api(symbol: str, date_from: str, date_to: str = None) -> dict
    @staticmethod
    def print_stock_prices(prices: dict) -> None
```

### ExcelService

```python
class ExcelService:
    def __init__(file_path: str)
    def create_excel() -> None
    def save_excel(dataframe: pd.DataFrame) -> bool
    def update_excel() -> None
    def print_excel_columns() -> None
```

### StockTrackerApplication

```python
class StockTrackerApplication:
    def __init__(excel_file_path: str)
    def run() -> None
    def create_new_excel_file() -> None
    def get_stock_data_for_symbol(symbol: str, date_from: str, date_to: str = None) -> dict
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure `keys.txt` exists in the correct location
   - Check API key format and validity

2. **Excel File Permission Error**
   - Close the Excel file before running the application
   - Ensure write permissions in the directory

3. **No Stock Data Returned**
   - Verify stock symbol is correct
   - Check date range is valid
   - Ensure API key has sufficient quota

### Error Messages

- `"API token not found"`: Check `api_credentials/keys.txt`
- `"Cannot save to file"`: Close Excel file and try again
- `"No data found for symbol"`: Verify symbol and date range

## 🤝 Contributing

1. Follow the established naming conventions
2. Add proper docstrings to all functions and classes
3. Test your changes before submitting
4. Update documentation as needed

## 📄 License

This project is for educational and personal use.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Ensure all dependencies are installed
4. Verify API keys are properly configured

---

**Note**: This is the refactored version of the original stock tracking application. The new version follows proper Python conventions and provides a more maintainable codebase. 