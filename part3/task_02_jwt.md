from flask_jwt_extended import create_access_token, set_access_claims
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask import request
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import get_jwt_identity, get_jwt_claims
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.get(identity)  # Assuming identity is the user ID
    return {'is_admin': user.is_admin}

@app.route('/login', methods=['POST'])
def login():
    # ... (Login logic to authenticate the user) ...
    user = User.query.filter_by(email=email).first()
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if not claims.get('is_admin', False):
                return jsonify({'message': 'Admin access required.'}), 403  # Forbidden
            else:
                return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/admin/users', methods=['POST'])
@admin_required()
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False) # Default to False

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    # Email validation (you might use a regex or a library like email-validator)
    if not validate_email(email):
        return jsonify({'message': 'Invalid email format.'}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered.'}), 409  # Conflict

    hashed_password = generate_password_hash(password).decode('utf-8')  # Hash the password
    new_user = User(email=email, password=hashed_password, is_admin=is_admin)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully.', 'user_id': new_user.id}), 201 # Created

@app.route('/admin/users/<int:user_id>', methods=['PUT', 'PATCH'])
@admin_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin')  # Allow changing admin status

    if email:
        if not validate_email(email):
            return jsonify({'message': 'Invalid email format.'}), 400
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({'message': 'Email already exists.'}), 409
        user.email = email
 if password:
        hashed_password = generate_password_hash(password).decode('utf-8')
        user.password = hashed_password

    if is_admin is not None:  # Allow explicitly setting is_admin to True/False
        user.is_admin = is_admin

    db.session.commit()
    return jsonify({'message': 'User updated successfully.'}), 200

@app.route('/places/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'message': 'Place not found'}), 404

    current_user_id = get_jwt_identity()
    claims = get_jwt_claims()

    if place.user_id != current_user_id and not claims.get('is_admin', False):
        return jsonify({'message': 'You are not authorized to update this place'}), 403

    # ... (Update place logic) ...

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'message': 'Review not found'}), 404

    current_user_id = get_jwt_identity()
    claims = get_jwt_claims()

    if review.user_id != current_user_id and not claims.get('is_admin', False):
        return jsonify({'message': 'You are not authorized to delete this review'}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200


