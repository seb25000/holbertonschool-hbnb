from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the amenity response model
amenity_response_model = api.inherit('AmenityResponse', amenity_model, {
    'id': fields.String(description='Unique identifier of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(500, 'Server error')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """List all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities]
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Server error')
    @api.marshal_with(amenity_response_model, code=201)
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(400, f"Missing required field: {str(e)}")
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

@api.route('/<amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.response(200, 'Success', amenity_response_model)
    @api.response(404, 'Amenity not found')
    @api.response(500, 'Server error')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, 'Amenity not found')
            return amenity.to_dict()
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity successfully updated', amenity_response_model)
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Server error')
    @api.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        """Update amenity details"""
        try:
            amenity_data = api.payload
            amenity = facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                api.abort(404, 'Amenity not found')
            return amenity.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(400, f"Missing required field: {str(e)}")
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")
            
    @api.doc('delete_amenity')
    @api.response(200, 'Amenity successfully deleted')
    @api.response(404, 'Amenity not found')
    @api.response(500, 'Server error')
    def delete(self, amenity_id):
        """Delete an amenity"""
        try:
            if facade.delete_amenity(amenity_id):
                return {'message': 'Amenity deleted successfully'}
            api.abort(404, 'Amenity not found')
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

@api.route('/places/<place_id>/amenities')
@api.param('place_id', 'The place identifier')
class PlaceAmenityList(Resource):
    @api.doc('get_place_amenities')
    @api.response(200, 'List of amenities for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.response(500, 'Server error')
    @api.marshal_list_with(amenity_response_model)
    def get(self, place_id):
        """Get all amenities for a specific place"""
        try:
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, 'Place not found')
            return [amenity.to_dict() for amenity in place.amenities]
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")