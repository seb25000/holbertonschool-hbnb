import os
from flask import Flask
def create_app(config):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    # Load configuration from the provided object
    app.config.from_object(config)

    # Example: Check if database URI is loaded.
    # You can add your logging or debugging lines to make sure config is correctly passed
    # app.logger.debug(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    # Example: Register blueprints (assuming you have them defined)
    # from . import routes  # Import your routes module
    # app.register_blueprint(routes.bp)  # Register your blueprint

    # More example for database:
    # from . import models
    # models.db.init_app(app)

    return app

# Example Usage (not part of app/__init__.py, this is for example purposes only)
# from config import DevelopmentConfig
# app = create_app(DevelopmentConfig)