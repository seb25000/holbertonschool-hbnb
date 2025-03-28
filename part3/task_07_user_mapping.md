# app/models/baseclass.py
from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

# app/models/user.py
from app import db, bcrypt
from .baseclass import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User email={self.email}>"

# app/persistence/repository.py
from app import db

class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def add(self, entity):
        db.session.add(entity)
        self.save()

    def get(self, id):
        return self.model.query.get(id)

    def list(self):
        return self.model.query.all()

    def update(self, entity):
        db.session.merge(entity)
        self.save()

    def delete(self, id):
        entity = self.get(id)
        if entity:
            db.session.delete(entity)
            self.save()

    def save(self):
        db.session.commit()

# app/persistence/repositories/user_repository.py
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

# app/services/facade.py
from app.persistence.repositories.user_repository import UserRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def list_users(self):
        return self.user_repo.list()

# app/api/v1/users.py
from flask import Blueprint, request, jsonify
from app.services.facade import HBnBFacade

bp = Blueprint('users', __name__, url_prefix='/api/v1/users')
facade = HBnBFacade()

@bp.route('/', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        data = request.get_json()
        try:
            user = facade.create_user(data)
            return jsonify({'id': user.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    elif request.method == 'GET':
        users = facade.list_users()
        user_list = [{'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name} for user in users]
        return jsonify(user_list), 200


@bp.route('/<id>', methods=['GET'])
def get_user(id):
    user = facade.get_user(id)
    if user:
        return jsonify({'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory database for testing.  For persistent storage, use a file-based DB.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable modification tracking
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from app.api.v1 import users

app.register_blueprint(users.bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create the tables
    app.run(debug=True)
