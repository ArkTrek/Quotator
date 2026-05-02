import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-ink-pen-secret-key-123')
    DEBUG = False
    TESTING = False
    DATABASE_FILE = os.environ.get('DATABASE_FILE', 'data.toon')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, we should definitely have a real secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
