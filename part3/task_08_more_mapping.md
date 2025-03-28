from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Column

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define SQLAlchemy models
class Place(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return f"<Place(title='{self.title}')>"


class Review(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(1000))
    rating = Column(Integer)  # Assuming a rating scale, e.g., 1 to 5

    def __repr__(self):
        return f"<Review(rating={self.rating})>"


class Amenity(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Amenity(name='{self.name}')>"


# Define repositories (basic CRUD operations)
class PlaceRepository:
    def create(self, title, description=None, price=None, latitude=None, longitude=None):
        place = Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude)
        db.session.add(place)
        db.session.commit()
        return place

    def get(self, id):
        return Place.query.get(id)

    def update(self, id, title=None, description=None, price=None, latitude=None, longitude=None):
        place = self.get(id)
        if place:
            if title:
                place.title = title
            if description:
                place.description = description
            if price:
                place.price = price
            if latitude:
                place.latitude = latitude
            if longitude:
                place.longitude = longitude
            db.session.commit()
            return place
        return None

    def delete(self, id):
        place = self.get(id)
        if place:
            db.session.delete(place)
            db.session.commit()
            return True
        return False


class ReviewRepository:
    def create(self, text, rating):
        review = Review(text=text, rating=rating)
        db.session.add(review)
        db.session.commit()
        return review

    def get(self, id):
        return Review.query.get(id)

    def update(self, id, text=None, rating=None):
        review = self.get(id)
        if review:
            if text:
                review.text = text
            if rating:
                review.rating = rating
            db.session.commit()
            return review
        return None

    def delete(self, id):
        review = self.get(id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False


class AmenityRepository:
    def create(self, name):
        amenity = Amenity(name=name)
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get(self, id):
        return Amenity.query.get(id)

    def update(self, id, name=None):
        amenity = self.get(id)
        if amenity:
            if name:
                amenity.name = name
            db.session.commit()
            return amenity
        return None

    def delete(self, id):
        amenity = self.get(id)
        if amenity:
            db.session.delete(amenity)
            db.session.commit()
            return True
        return False


# Define facade methods (example usage)
class Facade:
    def __init__(self):
        self.place_repository = PlaceRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()

    # Place operations
    def create_place(self, title, description=None, price=None, latitude=None, longitude=None):
        return self.place_repository.create(title, description, price, latitude, longitude)

    def get_place(self, id):
        return self.place_repository.get(id)

    def update_place(self, id, title=None, description=None, price=None, latitude=None, longitude=None):
        return self.place_repository.update(id, title, description, price, latitude, longitude)

    def delete_place(self, id):
        return self.place_repository.delete(id)

    # Review operations
    def create_review(self, text, rating):
        return self.review_repository.create(text, rating)

    def get_review(self, id):
        return self.review_repository.get(id)

    def update_review(self, id, text=None, rating=None):
        return self.review_repository.update(id, text, rating)

    def delete_review(self, id):
        return self.review_repository.delete(id)

    # Amenity operations
    def create_amenity(self, name):
        return self.amenity_repository.create(name)

    def get_amenity(self, id):
        return self.amenity_repository.get(id)

    def update_amenity(self, id, name=None):
        return self.amenity_repository.update(id, name)

    def delete_amenity(self, id):
        return self.amenity_repository.delete(id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables in the database

        # Example usage:
        facade = Facade()

        # Create a place
        place1 = facade.create_place(title="Cozy Cabin", description="A lovely cabin in the woods", price=120.0, latitude=34.0, longitude=-118.0)
        print(f"Created place: {place1}")

        # Get a place
        retrieved_place = facade.get_place(place1.id)
        print(f"Retrieved place: {retrieved_place}")

        # Update a place
        updated_place = facade.update_place(place1.id, title="Updated Cabin Title")
        print(f"Updated place: {updated_place}")

        # Create a review
        review1 = facade.create_review(text="Great place to stay!", rating=5)
        print(f"Created review: {review1}")

        # Create an amenity
        amenity1 = facade.create_amenity(name="WiFi")
        print(f"Created amenity: {amenity1}")

        # Delete a place
        delete_result = facade.delete_place(place1.id)
        print(f"Place deletion result: {delete_result}")
