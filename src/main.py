"""
Stock Tracker Main Entry Point

This is the main entry point for the Stock Tracker application.
It initializes and runs the stock tracking system.
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from stock_tracker.core.application import StockTrackerApplication


def setup_logging(verbose: bool = False):
    """
    Set up logging configuration for the application.
    
    Args:
        verbose: If True, enable debug level logging
    """
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"stock_tracker_{timestamp}.log"
    
    # Configure logging
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers to appropriate levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Log file: {log_file}")
    logger.info(f"Log level: {'DEBUG' if verbose else 'INFO'}")


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Stock Tracker Application - Track stock performance using Excel files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py chatGptStocks.xlsx
  python src/main.py my_portfolio.xlsx --create
  python src/main.py stocks.xlsx --verbose
  python src/main.py --help
        """
    )
    
    parser.add_argument(
        'filename',
        help='Excel file to process (e.g., chatGptStocks.xlsx)'
    )
    
    parser.add_argument(
        '--create',
        action='store_true',
        help='Create a new Excel file if it doesn\'t exist'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    return parser.parse_args()


def main():
    """
    Main function that initializes and runs the Stock Tracker application.
    
    This function:
    1. Parses command line arguments
    2. Sets up logging
    3. Sets up the Excel file path
    4. Creates the application instance
    5. Runs the stock tracking workflow
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Get the Excel file path
    excel_file = args.filename
    
    logger.info(f"Starting Stock Tracker Application")
    logger.info(f"Excel file: {excel_file}")
    logger.info(f"Create flag: {args.create}")
    logger.info(f"Verbose logging: {args.verbose}")
    
    try:
        # Create and run the application
        app = StockTrackerApplication(excel_file)
        
        # Check if file exists, create if requested
        if not os.path.exists(excel_file):
            if args.create:
                logger.info(f"Creating new Excel file: {excel_file}")
                print(f"Creating new Excel file: {excel_file}")
                app.create_new_excel_file()
            else:
                logger.error(f"Excel file not found: {excel_file}")
                print(f"Error: Excel file '{excel_file}' not found.")
                print("Use --create flag to create a new file, or ensure the file exists.")
                sys.exit(1)
        
        # Run the application
        logger.info("Starting application execution")
        app.run()
        logger.info("Application execution completed successfully")
        
    except FileNotFoundError as error:
        logger.error(f"File not found error: {error}")
        print(f"Error: Excel file '{excel_file}' not found.")
        print("Please ensure the Excel file exists in the project directory.")
        print(f"Details: {error}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\nApplication interrupted by user.")
        sys.exit(0)
        
    except Exception as error:
        logger.error(f"Unexpected error: {error}", exc_info=True)
        print(f"An unexpected error occurred: {error}")
        print("Please check your configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main() 