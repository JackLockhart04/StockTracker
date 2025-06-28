import os
import re
from pathlib import Path

class ApiKeyManager:
    _instance = None
    _keys = {}
    _keys_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiKeyManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._keys_loaded:
            self._load_keys()
            self._keys_loaded = True
    
    def _load_keys(self):
        """Load API keys from the keys.txt file"""
        try:
            # Get the path to keys.txt relative to the project root
            project_root = Path(__file__).parent.parent
            keys_file = project_root / "apiStuff" / "keys.txt"
            
            if not keys_file.exists():
                print(f"Warning: API keys file not found at {keys_file}")
                return
            
            with open(keys_file, 'r') as f:
                content = f.read()
            
            # Parse the keys using regex
            # Look for patterns like 'Service Name': KEY
            key_pattern = r"'([^']+)':\s*([A-Za-z0-9]+)"
            matches = re.findall(key_pattern, content)
            
            for service_name, key in matches:
                self._keys[service_name] = key
                print(f"Loaded API key for {service_name}")
                
        except Exception as e:
            print(f"Error loading API keys: {e}")
    
    def get_key(self, service_name):
        """Get API key for a specific service"""
        return self._keys.get(service_name)
    
    def get_stockdata_key(self):
        """Get the StockData.org API key specifically"""
        return self.get_key('StockData.org')
    
    def get_alphavantage_key(self):
        """Get the Alpha Vantage API key specifically"""
        return self.get_key('Alpha Vantage')
    
    def get_finnhub_key(self):
        """Get the Finnhub API key specifically"""
        return self.get_key('Finnhub')
    
    def list_services(self):
        """List all available services with keys"""
        return list(self._keys.keys())
    
    def has_key(self, service_name):
        """Check if a key exists for a service"""
        return service_name in self._keys

# Convenience functions for easy access
def get_api_key(service_name):
    """Get API key for a service"""
    manager = ApiKeyManager()
    return manager.get_key(service_name)

def get_stockdata_key():
    """Get StockData.org API key"""
    manager = ApiKeyManager()
    return manager.get_stockdata_key() 