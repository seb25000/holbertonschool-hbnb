from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    bcrypt = Bcrypt()
    
    #
    # Existent code with app Flask instance
    # ...
    bcrypt.init_app(app)

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    return app


    ########################################################
    
    import re
import hashlib
import os
from app.models.base import BaseModel
import uuid
from datetime import datetime

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.validate_name(first_name, "first_name")
        self.validate_name(last_name, "last_name")
        self.validate_email(email)
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store owned places
        
        # Gestion du mot de passe
        self.password_hash = None
        self.password_salt = None
        if password:
            self.set_password(password)

    @staticmethod
    def validate_name(name, field):
        """Validate name fields"""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field} is required and must be a string")
        if len(name) > 50:
            raise ValueError(f"{field} must not exceed 50 characters")

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        # Validation plus stricte de l'email
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Vérifier la présence d'au moins une lettre majuscule, une lettre minuscule et un chiffre
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one digit")

    def set_password(self, password):
        """Hash and set the password"""
        self.validate_password(password)
        
        # Générer un sel aléatoire
        self.password_salt = os.urandom(16).hex()
        
        # Hasher le mot de passe avec le sel
        self.password_hash = self._hash_password(password, self.password_salt)

    def verify_password(self, password):
        """Verify if the provided password matches the stored hash"""
        if not self.password_hash or not self.password_salt:
            return False
        
        hashed = self._hash_password(password, self.password_salt)
        return hashed == self.password_hash

    @staticmethod
    def _hash_password(password, salt):
        """Hash a password with the given salt"""
        return hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt.encode('utf-8'), 
            100000
        ).hex()

    def add_place(self, place):
        """Add a place to user's owned places"""
        if place not in self.places:
            self.places.append(place)

    def update(self, data):
        """Update user attributes with validation"""
        if 'first_name' in data:
            self.validate_name(data['first_name'], "first_name")
        if 'last_name' in data:
            self.validate_name(data['last_name'], "last_name")
        if 'email' in data:
            self.validate_email(data['email'])
        if 'password' in data:
            self.set_password(data['password'])
            # Supprimer le mot de passe en clair du dictionnaire pour éviter qu'il soit utilisé par super().update()
            del data['password']
        
        super().update(data)

    def to_dict(self):
        """Convert the object to a dictionary representation"""
        # Obtenir d'abord les attributs de base (id, created_at, updated_at)
        try:
            base_dict = super().to_dict()
        except Exception:
            # Si super().to_dict() échoue, créer un dictionnaire de base minimal
            base_dict = {
                'id': getattr(self, 'id', str(uuid.uuid4())),
                'created_at': getattr(self, 'created_at', datetime.now()).isoformat() if hasattr(self, 'created_at') else datetime.now().isoformat(),
                'updated_at': getattr(self, 'updated_at', datetime.now()).isoformat() if hasattr(self, 'updated_at') else datetime.now().isoformat()
            }
        
        # Définir les attributs spécifiques à l'utilisateur avec des valeurs par défaut sûres
        user_dict = {
            'first_name': getattr(self, 'first_name', None),
            'last_name': getattr(self, 'last_name', None),
            'email': getattr(self, 'email', None),
            'is_admin': getattr(self, 'is_admin', False),
            'places': []
        }
        
        # Fusionner les dictionnaires en donnant la priorité aux attributs utilisateur
        result = {**base_dict, **user_dict}
        
        # Supprimer explicitement les informations sensibles
        result.pop('password_hash', None)
        result.pop('password_salt', None)
        
        # Gérer la liste des places de manière sécurisée
        if hasattr(self, 'places') and self.places:
            try:
                result['places'] = [{
                    'id': place.id,
                    'name': place.name if hasattr(place, 'name') else place.title if hasattr(place, 'title') else "Unnamed Place"
                } for place in self.places if hasattr(place, 'id')]
            except Exception as e:
                # En cas d'erreur, garder une liste vide plutôt que de faire échouer la sérialisation
                result['places'] = []

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

        return result

#######################################################################################




