from .basemodel import BaseModel
from app.extensions import db
from .user import User

class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title: str, price: float, latitude: float, longitude: float, owner: User, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        """Title of a place."""
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        self.__title = value

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value):
        """Price of a place."""
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive.")
        self.__price = value

    @property
    def latitude(self):
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        """Latitude of the place"""
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        super().is_between("latitude", value, -90, 90)
        self.__latitude = value
    
    @property
    def longitude(self):
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        """Longitude of the place."""
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        super().is_between("longitude", value, -180, 180)
        self.__longitude = value

    @property
    def owner(self):
        return self.__owner
    
    @owner.setter
    def owner(self, value):
        """Name of the owner."""
        if not isinstance(value, User):
            raise TypeError("Owner must be a user instance")
        self.__owner = value

    def add_review(self, review):
        """Add a review."""
        self.reviews.append(review)
    
    def delete_review(self, review):
        """Delete a review."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity."""
        self.amenities.append(amenity)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id
        }
    
    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': self.amenities,
            'reviews': self.reviews
        }