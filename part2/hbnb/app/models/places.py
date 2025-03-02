from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Place class, to add a place or to modify one
    """
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self._title = title
        self.description = description
        self._price = price
        self._latitude = latitude
        self._longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []


    def validate(self):
        if not self.title or len(self.title) > 100:
            raise ValueError("Title is required and must be 100 characters or less")
        if self.price <= 0:
            raise ValueError("Price must be a positive value")
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")


    def add_review(self, review):
        """Add review to the place"""
        self.reviews.append(review)



    def add_amenity(self, amenity):
        """Add amenity to this place"""
        self.amenities.append(amenity)


    def __repr__(self):
        return f"<Place id={self.id} title={self.title}"


    def update(self, data):
        super().update(data)
        self.validate()