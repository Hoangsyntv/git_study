"""
Configuration management for KiotViet API
Loads settings from environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for KiotViet API"""
    
    # KiotViet API Settings
    RETAILER = os.getenv('KIOTVIET_RETAILER')
    CLIENT_ID = os.getenv('KIOTVIET_CLIENT_ID')
    CLIENT_SECRET = os.getenv('KIOTVIET_CLIENT_SECRET')
    BASE_URL = os.getenv('KIOTVIET_BASE_URL', 'https://public.kiotapi.com')
    AUTH_URL = os.getenv('KIOTVIET_AUTH_URL', 'https://id.kiotviet.vn/connect/token')
    
    # App Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate that all required config is present"""
        required_settings = [
            'RETAILER', 'CLIENT_ID', 'CLIENT_SECRET'
        ]
        
        missing = []
        for setting in required_settings:
            if not getattr(cls, setting):
                missing.append(f'KIOTVIET_{setting}')
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (hide sensitive data)"""
        print("🔧 Configuration:")
        print(f"  Retailer: {cls.RETAILER}")
        print(f"  Client ID: {cls.CLIENT_ID[:8]}..." if cls.CLIENT_ID else "  Client ID: Not set")
        print(f"  Client Secret: {'*' * 20}")
        print(f"  Base URL: {cls.BASE_URL}")
        print(f"  Debug: {cls.DEBUG}")
        print(f"  Cache: {cls.CACHE_ENABLED}")

# Validate config on import
try:
    Config.validate()
    if Config.DEBUG:
        Config.print_config()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    print("💡 Please check your .env file or environment variables")
