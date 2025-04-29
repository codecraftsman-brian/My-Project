"""
Configuration settings for the Telegram Message Scheduler application.
"""

import os

class Config:
    """Configuration settings for the application."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'telegram_scheduler_secret_key')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    
    # Application directories
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # File paths
    CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')
    MESSAGE_FILE = os.path.join(DATA_DIR, 'messages.json')
    SENT_LOG_FILE = os.path.join(DATA_DIR, 'sent_log.json')
    
    # Upload settings
    ALLOWED_EXTENSIONS = {'txt', 'csv'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size