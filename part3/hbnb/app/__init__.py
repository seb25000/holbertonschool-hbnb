from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager  # Importer JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from config import config

bcrypt = Bcrypt()  # Instancier Bcrypt
jwt = JWTManager()  # Instancier JWTManager

def create_app(config_name="default"):
    """
    Application factory function to create a Flask application instance.
    Accepts a configuration class and sets up the application accordingly.
    """

    # Créer l'instance de l'application Flask
    app = Flask(__name__)

    # Charger la configuration à partir du dictionnaire 'config'
    app.config.from_object(config[config_name])

    # Ajouter la clé secrète pour JWT
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'your_jwt_secret_key')  # Utilise SECRET_KEY si défini dans config

    # Initialiser Bcrypt avec l'application
    bcrypt.init_app(app)

    # Initialiser JWT avec l'application
    jwt.init_app(app)

    # Créer l'instance de l'API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Ajouter les namespaces de l'API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
