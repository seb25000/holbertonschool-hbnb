from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from app.services import facade

api = Namespace('admin', description='Admin operations')

@api.route('/users/')
class AdminUserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User created successfully")
    @api.response(400, "Email already registered")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Register a new user as the admin"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/users/<int:user_id>')
class AdminUser(Resource):
    @api.expect(user_model)
    @api.response(200, "User updated successfully")
    @api.response(404, "User not found")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def put(self, user_id):
        """Modify user information as the admin"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        try:
            updated_user = facade.update_user(user_id, data)
            return updated_user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/amenities/')
class AdminAmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity created successfully")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Register new amenity as the admin"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            new_amenity = facade.create_amenity(api.payload)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/amenities/<int:amenity_id>')
class AdminAmenity(Resource):
    @api.expect(amenity_model)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def put(self, amenity_id):
        """Modify amenity details as the admin"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404

        try:
            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            return updated_amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/places/<int:place_id>')
class AdminPlace(Resource):
    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def put(self, place_id):
        """Modify place information as the admin"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not current_user.get('is_admin') and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(204, "Place deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def delete(self, place_id):
        """Delete a place as the admin"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not current_user.get('is_admin') and place.owner_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_place(place_id)
            return '', 204
        except Exception as e:
            return {'error': str(e)}, 500
