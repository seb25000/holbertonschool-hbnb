from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for example
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Association table for Place and Amenity (Many-to-Many relationship)
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    # Relationship with Place (One-to-Many)
    places = db.relationship('Place', backref='user', lazy=True)
    # Relationship with Review (One-to-Many)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}')"

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    number_rooms = db.Column(db.Integer, default=0)
    number_bathrooms = db.Column(db.Integer, default=0)
    max_guest = db.Column(db.Integer, default=0)
    price_by_night = db.Column(db.Integer, default=0)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Relationship with Review (One-to-Many)
    reviews = db.relationship('Review', backref='place', lazy=True)
    # Relationship with Amenity (Many-to-Many)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True))

    def __repr__(self):
        return f"Place(id={self.id}, name='{self.name}')"

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"Review(id={self.id}, text='{self.text[:20]}...')"

class Amenity(db.Model):
    __tablename__ = 'amenities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Amenity(id={self.id}, name='{self.name}')"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create some sample data
        user1 = User(email='test@example.com', password='password', first_name='Test', last_name='User')
        user2 = User(email='test2@example.com', password='password', first_name='Test2', last_name='User2')
        db.session.add_all([user1, user2])
        db.session.commit()

        place1 = Place(user_id=user1.id, name='Cozy Apartment', description='A nice place to stay')
        place2 = Place(user_id=user1.id, name='Luxury Villa', description='A luxurious villa')
        place3 = Place(user_id=user2.id, name='Budget Room', description='A cheap but comfortable room')

        db.session.add_all([place1, place2, place3])
        db.session.commit()

        review1 = Review(place_id=place1.id, user_id=user1.id, text='Great place!', rating=5)
        review2 = Review(place_id=place1.id, user_id=user2.id, text='Very clean and comfortable', rating=4)
        review3 = Review(place_id=place2.id, user_id=user1.id, text='Amazing experience', rating=5)

        db.session.add_all([review1, review2, review3])
        db.session.commit()

        amenity1 = Amenity(name='WiFi')
        amenity2 = Amenity(name='Swimming Pool')
        db.session.add_all([amenity1, amenity2])
        db.session.commit()

        place1.amenities.append(amenity1)
        place2.amenities.append(amenity2)
        place2.amenities.append(amenity1)
        db.session.commit()

        # Example queries demonstrating relationships
        print("User1's places:", user1.places)
        print("Place1's reviews:", place1.reviews)
        print("Place2's amenities:", place2.amenities)
        print("Amenity1's places:", amenity1.places)
