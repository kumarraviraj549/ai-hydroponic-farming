"""Configuration settings for HydroAI Flask application."""

import os
from datetime import timedelta


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hydroai-secret-key-change-in-production')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://hydroai:password@localhost:5432/hydroai_dev'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # API settings
    API_VERSION = 'v1'
    PAGINATION_PER_PAGE = 20
    MAX_PAGINATION_PER_PAGE = 100
    
    # ML Model settings
    ML_MODEL_PATH = os.environ.get('ML_MODEL_PATH', 'ml_models/')
    PREDICTION_CACHE_TTL = 300  # 5 minutes
    
    # Alert settings
    ALERT_EMAIL_ENABLED = True
    ALERT_SMS_ENABLED = False
    

class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    TESTING = False
    
    # Development database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'sqlite:///hydroai_dev.db'
    )
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    

class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Production database (required)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is required in production")
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = 'INFO'
    

class TestingConfig(Config):
    """Testing configuration."""
    
    DEBUG = True
    TESTING = True
    
    # In-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable JWT for easier testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)
    
    # Disable alerts in testing
    ALERT_EMAIL_ENABLED = False
    ALERT_SMS_ENABLED = False
    
    # Logging
    LOG_LEVEL = 'ERROR'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
