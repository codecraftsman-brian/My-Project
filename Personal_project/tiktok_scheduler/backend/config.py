import os
from datetime import timedelta

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration"""
    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', f'sqlite:///{os.path.join(basedir, "tiktok_scheduler.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB max upload
    ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}
    
    # TikTok API settings
    TIKTOK_CLIENT_KEY = os.environ.get('TIKTOK_CLIENT_KEY')
    TIKTOK_CLIENT_SECRET = os.environ.get('TIKTOK_CLIENT_SECRET')
    TIKTOK_REDIRECT_URI = os.environ.get('TIKTOK_REDIRECT_URI')
    
    # Encryption settings
    ENCRYPTION_MASTER_KEY = os.environ.get('ENCRYPTION_MASTER_KEY')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # In production, ensure these are set in the environment
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}