# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key' # use os.environ for prod to set it
    DEBUG = False  # Turn debugging off by default for security
    # Add other configuration variables here (e.g., database settings)

class DevelopmentConfig(Config):
    DEBUG = True
    # database configuration for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'  # Example
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    # database configuration for production
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # Use env var for production

    # Add settings specific to production (e.g., more secure secret key,
    # different database URL, logging configuration)
