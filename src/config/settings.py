"""Settings configuration for the Master Agent system."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
LOG_DIR = BASE_DIR / 'logs'
CONFIG_DIR = BASE_DIR / 'config'

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# API Keys
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_API_SECRET = os.getenv('ALPACA_API_SECRET')
ALPACA_PAPER_TRADING = os.getenv('ALPACA_PAPER_TRADING', 
'true').lower() == 'true'

# Database Configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'masteragent')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'masteragent')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'project3')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))

# Redis Configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# System Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

