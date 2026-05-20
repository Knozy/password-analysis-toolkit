import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///password_analysis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'txt', 'csv'}
    
    # Password analysis settings
    MIN_PASSWORD_LENGTH = 1  # For testing
    MAX_PASSWORD_LENGTH = 255
    MIN_ENTROPY_THRESHOLD = 40  # bits
    STRONG_ENTROPY_THRESHOLD = 80  # bits
    
    # Attack simulation settings
    MAX_WORDLIST_SIZE = 1_000_000
    MAX_SIMULATION_ATTEMPTS = 100_000
    
    # Logging
    LOG_DIR = 'app/data/logs'
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
