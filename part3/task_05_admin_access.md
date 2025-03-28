from flask import request
from flask_restx import Namespace, Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt  # Import Bcrypt

# Assuming facade is an object that handles database interactions
# You'll need to adapt this to your specific implementation
# from your_module import facade

# Replace with your actual facade implementation
class MockFacade:
    def __init__(self):
        self.users = {}
        self.amenities = {}
        self.places = {}
        self.reviews = {}
        self.next_user_id = 1
        self.next_amenity_id = 1
        self.next_place_id = 1
        self.next_review_id = 1

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_user_by_email(self, email):
        for user_id, user in self.users.items():
            if user['email'] == email:
                return user
        return None

    def create_user(self, user_data):
        user_id = self.next_user_id
        self.next_user_id += 1
        user_data['id'] = user_id
        self.users[user_id] = user_data
        return user_data

    def update_user(self, user_id, user_data):
        if user_id in self.users:
            self.users[user_id].update(user_data)
            return self.users[user_id]
        return None

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def create_amenity(self, amenity_data):
        amenity_id = self.next_amenity_id
        self.next_amenity_id += 1
        amenity_data['id'] = amenity_id
        self.amenities[amenity_id] = amenity_data
        return amenity_data

    def update_amenity(self, amenity_id, amenity_data):
        if amenity_id in self.amenities:
            self.amenities[amenity_id].update(amenity_data)
            return self.amenities[amenity_id]
        return None
    
    def get_place(self, place_id):
      return self.places.get(place_id)

    def update_place(self, place_id, place_data):
        if place_id in self.places:
            self.places[place_id].update(place_data)
            return self.places[place_id]
        return None

facade = MockFacade()
bcrypt = Bcrypt()  # Initialize Bcrypt


api = Namespace('admin', description='Admin operations')

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt() # Changed from get_jwt_identity() to get_jwt() to retrieve the entire payload
        if not current_user.get('is_admin'):  # Access 'is_admin' directly from the payload
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')
        password = user_data.get('password')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_data['password'] = hashed_password

        new_user = facade.create_user(user_data)
        return new_user, 201  # Return 201 Created status code


@api.route('/users/<int:user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt()  # Changed from get_jwt_identity() to get_jwt()
        if not current_user.get('is_admin'):  # Access 'is_admin' directly from the payload
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        password = data.get('password')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user['id'] != user_id:  # Access id from the dictionary
                return {'error': 'Email already in use'}, 400

        # Hash the password if a new password is provided
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            data['password'] = hashed_password

        updated_user = facade.update_user(user_id, data)
        if updated_user:
            return updated_user, 200
        else:
            return {'error': 'User not found'}, 404


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt()  # Changed from get_jwt_identity() to get_jwt()
        if not current_user.get('is_admin'):  # Access 'is_admin' directly from the payload
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        new_amenity = facade.create_amenity(amenity_data)
        return new_amenity, 201


@api.route('/amenities/<int:amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt()  # Changed from get_jwt_identity() to get_jwt()
        if not current_user.get('is_admin'):  # Access 'is_admin' directly from the payload
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if updated_amenity:
            return updated_amenity, 200
        else:
            return {'error': 'Amenity not found'}, 404

@api.route('/places/<int:place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')  # Assuming user ID is also in the JWT

        place = facade.get_place(place_id)
        if not place:
          return {'error': 'Place not found'}, 404

        if not is_admin and place.get('owner_id') != user_id: # Access 'owner_id' from the dictionary
            return {'error': 'Unauthorized action'}, 403

        place_data = request.json
        updated_place = facade.update_place(place_id, place_data)

        if updated_place:
            return updated_place, 200
        else:
            return {'error': 'Place not found'}, 404