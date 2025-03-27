from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask_bcrypt import Bcrypt  # For password hashing
from datetime import timedelta
# Assuming you have these models and database setup
# from models import User, Place, Review, db

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "super-secret"  # Change this in production!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) # set expiry
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Placeholder for your database initialization
# db.init_app(app)

# Example User Model (replace with your actual model)
class User:  # Replace with your actual SQLAlchemy User model
    def __init__(self, email, password, is_admin=False, id=None):
        self.id = id
        self.email = email
        self.password = password  # Hashed password
        self.is_admin = is_admin

    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'is_admin': self.is_admin}

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def query(cls):
      # dummy db
      users = [
          User("test@example.com",bcrypt.generate_password_hash("password").decode('utf-8'), False, 1),
          User("admin@example.com",bcrypt.generate_password_hash("password").decode('utf-8'), True, 2)
      ]
      class DummyQuery:
        def filter_by(self, email=None):
          for u in users:
            if u.email == email:
              return u
          return None
        def get(self, id):
          for u in users:
            if u.id == id:
              return u
          return None

      return DummyQuery()


class Place:
  def __init__(self, name, user_id, description="", id=None):
    self.id = id
    self.name = name
    self.user_id = user_id
    self.description = description

  def to_dict(self):
    return {"id": self.id, "name": self.name, "user_id": self.user_id, "description": self.description}
  @classmethod
  def query(cls):
    places = [
      Place("My Place", 1, "a nice place", 1),
      Place("Admin's Place", 2, "an admin place", 2)
    ]
    class DummyQuery:
      def get(self, id):
        for p in places:
          if p.id == id:
            return p
        return None
    return DummyQuery()

# Custom Decorator for Admin Access
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()  # Ensure JWT is present and valid
            claims = get_jwt()
            if claims.get('is_admin'):
                return fn(*args, **kwargs)
            else:
                return jsonify({'message': 'Admin access required'}), 403  # Forbidden
        return decorator
    return wrapper


# Callback function to add custom claims to the JWT
@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.get(identity)  # Fetch user from database
    if user:
        return {'is_admin': user.is_admin}  # Add 'is_admin' claim
    return {'is_admin': False}  # Default to False if user not found



# Authentication Endpoint
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)  # Use User ID as identity
        return jsonify(access_token=access_token)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# Admin-Only Endpoint: Create User
@app.route('/admin/users', methods=['POST'])
@jwt_required()
@admin_required()
def create_user():
    email = request.json.get('email')
    password = request.json.get('password')
    is_admin = request.json.get('is_admin', False)  # Default to False

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already in use'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, password=hashed_password, is_admin=is_admin)
    # db.session.add(new_user)
    # db.session.commit()
    new_user.id = 3 # dummy, usually auto-increment

    return jsonify({'message': 'User created successfully', 'user': new_user.to_dict()}), 201


# Admin-Only Endpoint: Modify User
@app.route('/admin/users/<user_id>', methods=['PUT'])
@jwt_required()
@admin_required()
def modify_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    email = request.json.get('email')
    password = request.json.get('password')
    is_admin = request.json.get('is_admin')

    if email:
        # Check if the new email is already in use by another user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != int(user_id): #check id because PUT to the same user
            return jsonify({'message': 'Email already in use'}), 400
        user.email = email

    if password:
        user.set_password(password) # hash password

    if is_admin is not None:
        user.is_admin = is_admin

    # db.session.commit()

    return jsonify({'message': 'User updated successfully', 'user': user.to_dict()}), 200


# Example: Modifying a Place (with admin bypass)
@app.route('/places/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    claims = get_jwt()
    current_user_id = get_jwt_identity()  # Assuming this returns the user's ID

    place = Place.query.get(place_id)
    if not place:
        return jsonify({'message': 'Place not found'}), 404

    if claims.get('is_admin') == True:
        # Admin can modify any place
        pass  # Allow the update to proceed
    elif place.user_id != current_user_id:
        return jsonify({'message': 'You do not have permission to modify this place'}), 403
    #  rest of update logic
    place.name = request.json.get('name', place.name)
    place.description = request.json.get('description', place.description)
    # db.session.commit()
    return jsonify(place.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)
