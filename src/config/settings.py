import os
from datetime import timedelta

# Flask Application Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Mining Settings
DEFAULT_MINING_POOL = os.environ.get('DEFAULT_MINING_POOL', 'stratum+tcp://pool.systm.org:22550')  # Dogecoin pool
DEFAULT_WALLET = os.environ.get('DEFAULT_WALLET', '')
MINING_ALGORITHM = 'scrypt'  # Dogecoin uses scrypt algorithm
DEFAULT_THREADS = int(os.environ.get('DEFAULT_THREADS', '2'))
MINING_COIN = 'DOGE'

# System Monitoring Settings
MONITORING_INTERVAL = int(os.environ.get('MONITORING_INTERVAL', '5'))  # seconds
TEMPERATURE_WARNING = int(os.environ.get('TEMPERATURE_WARNING', '70'))  # Celsius

# Security Settings
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

def load_config():
    """Load configuration from environment variables"""
    return {
        'SECRET_KEY': SECRET_KEY,
        'DEBUG': DEBUG,
        'DEFAULT_MINING_POOL': DEFAULT_MINING_POOL,
        'DEFAULT_WALLET': DEFAULT_WALLET,
        'MINING_ALGORITHM': MINING_ALGORITHM,
        'DEFAULT_THREADS': DEFAULT_THREADS,
        'MINING_COIN': MINING_COIN,
        'MONITORING_INTERVAL': MONITORING_INTERVAL,
        'TEMPERATURE_WARNING': TEMPERATURE_WARNING
    }