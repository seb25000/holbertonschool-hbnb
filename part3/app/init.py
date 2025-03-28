from flask import Flask
from config import Config

def create_app(config_class=Config):
    """Creates and configures the Flask app.

    Args:
        config_class: The configuration class to use. Defaults to Config.

    Returns:
        A Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints and other extensions here
    # Example:
    # from app.routes import bp as routes_bp
    # app.register_blueprint(routes_bp)

    return app
