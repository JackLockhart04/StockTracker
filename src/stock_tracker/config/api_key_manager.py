"""
API Key Management Module

This module provides a singleton class for managing API keys from external services.
It loads keys from a configuration file and provides easy access to them.
"""

import os
import re
import logging
from pathlib import Path
from typing import Optional, Dict, List

# Configure logging for this module
logger = logging.getLogger(__name__)


class ApiKeyManager:
    """
    Singleton class for managing API keys from external services.
    
    This class ensures only one instance exists and provides centralized
    access to API keys loaded from a configuration file.
    """
    
    _instance: Optional['ApiKeyManager'] = None
    _keys: Dict[str, str] = {}
    _keys_loaded: bool = False
    
    def __new__(cls) -> 'ApiKeyManager':
        """Ensure only one instance of ApiKeyManager exists."""
        if cls._instance is None:
            cls._instance = super(ApiKeyManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the API key manager and load keys if not already loaded."""
        if not self._keys_loaded:
            self._load_keys()
            self._keys_loaded = True
    
    def _load_keys(self) -> None:
        """
        Load API keys from the configuration file.
        
        Reads keys from the keys.txt file in the api_credentials directory
        and parses them using regex patterns.
        """
        try:
            # Get the path to keys.txt relative to the project root
            project_root = Path(__file__).parent.parent.parent.parent
            keys_file = project_root / "src" / "stock_tracker" / "config" / "api_credentials" / "keys.txt"
            
            logger.info(f"Loading API keys from: {keys_file}")
            
            if not keys_file.exists():
                logger.warning(f"API keys file not found at {keys_file}")
                print(f"Warning: API keys file not found at {keys_file}")
                return
            
            with open(keys_file, 'r') as file:
                content = file.read()
            
            logger.info(f"Read {len(content)} characters from keys file")
            
            # Parse the keys using regex
            # Look for patterns like 'Service Name': KEY
            key_pattern = r"'([^']+)':\s*([A-Za-z0-9]+)"
            matches = re.findall(key_pattern, content)
            
            logger.info(f"Found {len(matches)} API key patterns in file")
            
            for service_name, key in matches:
                self._keys[service_name] = key
                logger.info(f"Loaded API key for {service_name}")
                print(f"Loaded API key for {service_name}")
                
            logger.info(f"Successfully loaded {len(self._keys)} API keys")
                
        except Exception as error:
            logger.error(f"Error loading API keys: {error}")
            print(f"Error loading API keys: {error}")
    
    def get_key(self, service_name: str) -> Optional[str]:
        """
        Get API key for a specific service.
        
        Args:
            service_name: Name of the service to get the key for
            
        Returns:
            API key string if found, None otherwise
        """
        key = self._keys.get(service_name)
        if key:
            logger.debug(f"Retrieved API key for {service_name}")
        else:
            logger.warning(f"No API key found for service: {service_name}")
        return key
    
    def get_stockdata_key(self) -> Optional[str]:
        """
        Get the StockData.org API key specifically.
        
        Returns:
            StockData.org API key if found, None otherwise
        """
        return self.get_key('StockData.org')
    
    def get_alphavantage_key(self) -> Optional[str]:
        """
        Get the Alpha Vantage API key specifically.
        
        Returns:
            Alpha Vantage API key if found, None otherwise
        """
        return self.get_key('Alpha Vantage')
    
    def get_finnhub_key(self) -> Optional[str]:
        """
        Get the Finnhub API key specifically.
        
        Returns:
            Finnhub API key if found, None otherwise
        """
        return self.get_key('Finnhub')
    
    def list_services(self) -> List[str]:
        """
        List all available services with keys.
        
        Returns:
            List of service names that have keys configured
        """
        services = list(self._keys.keys())
        logger.info(f"Available services with keys: {services}")
        return services
    
    def has_key(self, service_name: str) -> bool:
        """
        Check if a key exists for a service.
        
        Args:
            service_name: Name of the service to check
            
        Returns:
            True if key exists, False otherwise
        """
        has_key = service_name in self._keys
        logger.debug(f"Service {service_name} has key: {has_key}")
        return has_key


# Convenience functions for easy access
def get_api_key(service_name: str) -> Optional[str]:
    """
    Get API key for a service.
    
    Args:
        service_name: Name of the service to get the key for
        
    Returns:
        API key string if found, None otherwise
    """
    manager = ApiKeyManager()
    return manager.get_key(service_name)


def get_stockdata_key() -> Optional[str]:
    """
    Get StockData.org API key.
    
    Returns:
        StockData.org API key if found, None otherwise
    """
    manager = ApiKeyManager()
    return manager.get_stockdata_key() 