from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude, user):
        super().__init__()
        self.validate_name(name)
        self.validate_price(price_by_night)
        self.validate_coordinates(latitude, longitude)
        self.validate_number(number_rooms, "number_rooms")
        self.validate_number(number_bathrooms, "number_bathrooms")
        self.validate_number(max_guest, "max_guest")
        
        self.name = name
        self.title = name  # Pour compatibilité avec le code existant
        self.description = description or ""  # Optional field
        self.number_rooms = int(number_rooms)
        self.number_bathrooms = int(number_bathrooms)
        self.max_guest = int(max_guest)
        self.price_by_night = float(price_by_night)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.user = user
        self.owner = user  # Pour compatibilité avec le code existant
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        
        # Add this place to the owner's places
        user.add_place(self)

    @staticmethod
    def validate_name(name):
        """Validate name field"""
        if not name or not isinstance(name, str):
            raise ValueError("Name is required and must be a string")
        if len(name) > 100:
            raise ValueError("Name must not exceed 100 characters")

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

    @staticmethod
    def validate_number(value, field_name):
        """Validate numeric fields"""
        try:
            value = int(value)
            if value < 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must be a non-negative integer")

    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
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
        if 'name' in data:
            self.validate_name(data['name'])
            data['title'] = data['name']  # Synchroniser title avec name
        elif 'title' in data:
            self.validate_name(data['title'])
            data['name'] = data['title']  # Synchroniser name avec title
            
        if 'price_by_night' in data:
            self.validate_price(data['price_by_night'])
        
        if 'latitude' in data or 'longitude' in data:
            lat = data.get('latitude', self.latitude)
            lon = data.get('longitude', self.longitude)
            self.validate_coordinates(lat, lon)
            
        if 'number_rooms' in data:
            self.validate_number(data['number_rooms'], "number_rooms")
            
        if 'number_bathrooms' in data:
            self.validate_number(data['number_bathrooms'], "number_bathrooms")
            
        if 'max_guest' in data:
            self.validate_number(data['max_guest'], "max_guest")
        
        super().update(data)

    def to_dict(self):
        """Convert the object to a dictionary representation"""
        result = super().to_dict()
        # Convert owner to dict
        if hasattr(self, 'user'):
            result['owner'] = self.user.to_dict()
            result['user'] = self.user.to_dict()
        # Convert amenities to list of dicts
        if hasattr(self, 'amenities'):
            result['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        # Convert reviews to list of dicts but with minimal information to avoid circular references
        if hasattr(self, 'reviews'):
            result['reviews'] = [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                }
            } for review in self.reviews]
        return result