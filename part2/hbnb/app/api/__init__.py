from flask import Flask, Blueprint
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as reviews_ns

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    api_bp,
    version='1.0',
    title='HBnB API',
    description='API for HBnB application'
)


api.add_namespace(place_ns, path='api/v1/places')
api.add_namespace(users_ns, path='api/v1/users')
api.add_namespace(amenities_ns, path='api/v1/amenities')
api.add_namespace(reviews_ns, path='api/v1/reviews')