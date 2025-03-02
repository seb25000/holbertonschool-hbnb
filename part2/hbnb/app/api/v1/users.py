from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=False, description='User password (only used for creation/update, never returned)')
})

# Define the place model for user responses
place_model = api.model('UserPlace', {
    'id': fields.String(description='Place ID'),
    'name': fields.String(description='Name of the place')
})

# Define the user response model
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='Unique identifier of the user'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Whether the user is an administrator'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
    'places': fields.List(fields.Nested(place_model), description='Places owned by the user')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.response(200, 'List of users retrieved successfully')
    @api.response(500, 'Server error')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """List all users"""
        try:
            users = facade.get_all_users()
            return [user.to_dict() for user in users]
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Server error')
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Create a new user"""
        try:
            user_data = api.payload
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(400, f"Missing required field: {str(e)}")
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'Success', user_response_model)
    @api.response(404, 'User not found')
    @api.response(500, 'Server error')
    @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            if not user:
                api.abort(404, 'User not found')
            return user.to_dict()
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'User successfully updated', user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Server error')
    @api.marshal_with(user_response_model)
    def put(self, user_id):
        """Update user details"""
        try:
            user_data = api.payload
            user = facade.update_user(user_id, user_data)
            if not user:
                api.abort(404, 'User not found')
            return user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(400, f"Missing required field: {str(e)}")
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")
            
    @api.doc('delete_user')
    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    @api.response(500, 'Server error')
    def delete(self, user_id):
        """Delete a user"""
        try:
            if facade.delete_user(user_id):
                return {'message': 'User deleted successfully'}
            api.abort(404, 'User not found')
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")

@api.route('/<user_id>/places')
@api.param('user_id', 'The user identifier')
class UserPlaceList(Resource):
    @api.doc('get_user_places')
    @api.response(200, 'List of places for the user retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(500, 'Server error')
    @api.marshal_list_with(place_model)
    def get(self, user_id):
        """Get all places for a specific user"""
        try:
            user = facade.get_user(user_id)
            if not user:
                api.abort(404, 'User not found')
            return user.to_dict().get('places', [])
        except Exception as e:
            api.abort(500, f"Server error: {str(e)}")