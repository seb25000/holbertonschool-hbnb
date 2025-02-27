from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.validate_title(title)
        self.validate_price(price)
        self.validate_coordinates(latitude, longitude)
        
        self.title = title
        self.description = description or ""  # Optional field
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        
        # Add this place to the owner's places
        owner.add_place(self)

    @staticmethod
    def validate_title(title):
        """Validate title field"""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_price(price):
        """Validate price field"""
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Price must be a positive number")

    @staticmethod
    def validate_coordinates(latitude, longitude):
        """Validate geographic coordinates"""
        try:
            lat = float(latitude)
            lon = float(longitude)
            if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180")

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def update(self, data):
        """Update place attributes with validation"""
        if 'title' in data:
            self.validate_title(data['title'])
        if 'price' in data:
            self.validate_price(data['price'])
        if 'latitude' in data or 'longitude' in data:
            lat = data.get('latitude', self.latitude)
            lon = data.get('longitude', self.longitude)
            self.validate_coordinates(lat, lon)
        
        super().update(data)

    def to_dict(self):
        """Convert the object to a dictionary representation"""
        result = super().to_dict()
        # Convert owner to dict
        if hasattr(self, 'owner'):
            result['owner'] = self.owner.to_dict()
        # Convert amenities to list of dicts
        if hasattr(self, 'amenities'):
            result['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        # Convert reviews to list of dicts
        if hasattr(self, 'reviews'):
            result['reviews'] = [review.to_dict() for review in self.reviews]
        return result
