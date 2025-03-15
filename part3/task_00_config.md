#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
importlib.metadata.version("flask-sqlalchemy")

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config.from_object(config_class)
    app.config.from_pyfile(config_filename)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # ajout import
    from yourapplication.model import db
    db.init_app(app)

    from config_class.views.admin import admin
    from config_class.views.frontend import frontend
    from flask import current_app, Blueprint, render_template
    admin = Blueprint('admin', __name__, url_prefix='/admin')
    @admin.route('/')
    def index():
    return render_template(current_app.config['INDEX_TEMPLATE'])
    app.register_blueprint(admin)
    app.register_blueprint(frontend)
    # fin ajout import
    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_pyfile(config_class)

    db = SQLAlchemy(app)

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_pyfile(config_class)

    from config_class.model import db
    db.init_app(app)

    return app
