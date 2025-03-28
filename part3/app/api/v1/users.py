from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from flask import request


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Admin status (true for admin)')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        admin_exists = facade.admin_verification()

        if not admin_exists:
            user_data['is_admin']=True
        else:
            if user_data.get('is_admin', False):
                try:
                    verify_jwt_in_request()
                    current_user_claims = get_jwt()
                    if not current_user_claims.get('is_admin', False):
                        return {'error': 'Admin privileges required'}, 403
                except Exception as e:
                    return {'error': 'Authentication required'}, 401
            else:
                user_data.pop('is_admin', None)

        
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
    
    @jwt_required()
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        users = facade.get_users()
        return [user.to_dict() for user in users], 200
    
@api.route('/login')
class UserLogin(Resource):
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token"""
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = facade.get_user_by_email(email)
        if user and user.check_password(password):
            access_token = create_access_token(identity={"id": user.id, "is_admin": user.is_admin})
            return jsonify(access_token=access_token), 200
        
        return {"error": "Invalid credentials"}, 401
    
@api.route('/<int:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID (Admin or owner only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin') and current_user['id'] != user_id:
            return {'error': 'Unauthorized'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_user = get_jwt_identity()

        if user_id != current_user['id']:
            return {'error': 'Unauthorized'}, 403

        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if 'email' in user_data or 'password' in user_data:
            return {"error": "You cannot modify email or password"}, 400

        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
