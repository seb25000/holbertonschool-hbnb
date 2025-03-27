# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # Use environment variable for production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'  # Example database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications (performance)


class DevelopmentConfig(Config):
    DEBUG = True
    # Further settings specific to the development environment

class ProductionConfig(Config):
    DEBUG = False
    # Further settings specific to the production environment
