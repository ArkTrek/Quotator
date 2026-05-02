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
    
    # Ollama Configuration
    OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/api/generate')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2.5-coder:1.5b')

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
