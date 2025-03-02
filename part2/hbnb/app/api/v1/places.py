from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email address'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

# Define the review model for place responses
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user': fields.Nested(api.model('ReviewUser', {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(description='First name'),
        'last_name': fields.String(description='Last name')
    }), description='User who wrote the review')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'name': fields.String(required=True, description='Name of the place'),
    'description': fields.String(description='Description of the place'),
    'number_rooms': fields.Integer(required=True, description='Number of rooms'),
    'number_bathrooms': fields.Integer(required=True, description='Number of bathrooms'),
    'max_guest': fields.Integer(required=True, description='Maximum number of guests'),
    'price_by_night': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'user_id': fields.String(required=True, description='ID of the owner'),
    'amenity_ids': fields.List(fields.String, description="List of amenities ID's")
})

# Define the place response model
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Unique identifier of the place'),
    'name': fields.String(description='Name of the place'),
    'description': fields.String(description='Description of the place'),
    'number_rooms': fields.Integer(description='Number of rooms'),
    'number_bathrooms': fields.Integer(description='Number of bathrooms'),
    'max_guest': fields.Integer(description='Maximum number of guests'),
    'price_by_night': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model)
    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places]

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created', place_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner or amenity not found')
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        """Register a new place"""
        place_data = api.payload

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(400, f"Missing required field: {str(e)}")
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.response(200, 'Success', place_response_model)
    @api.response(404, 'Place not found')
    @api.marshal_with(place_response_model)
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict()

    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Place successfully updated', place_response_model)
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(place_response_model)
    def put(self, place_id):
        """Update place details"""
        place_data = api.payload
        
        try:
            place = facade.update_place(place_id, place_data)
            if not place:
                api.abort(404, 'Place not found')
            return place.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(400, f"Missing required field: {str(e)}")
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

    @api.doc('delete_place')
    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        try:
            if facade.delete_place(place_id):
                return {'message': 'Place deleted successfully'}
            api.abort(404, 'Place not found')
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

@api.route('/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews]
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")