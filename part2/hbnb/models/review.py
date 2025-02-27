from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.validate_text(text)
        self.validate_rating(rating)
        
        self.text = text
        self.rating = int(rating)
        self.place = place
        self.user = user
        
        # Add this review to the place's reviews
        place.add_review(self)

    @staticmethod
    def validate_text(text):
        """Validate review text"""
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")

    @staticmethod
    def validate_rating(rating):
        """Validate rating value"""
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer between 1 and 5")

    def update(self, data):
        """Update review attributes with validation"""
        if 'text' in data:
            self.validate_text(data['text'])
        if 'rating' in data:
            self.validate_rating(data['rating'])
        
        super().update(data)

    def to_dict(self):
        """Convert the object to a dictionary representation"""
        result = super().to_dict()
        # Convert user to dict
        if hasattr(self, 'user'):
            result['user'] = self.user.to_dict()
        # Convert place to minimal dict to avoid circular references
        if hasattr(self, 'place'):
            result['place'] = {
                'id': self.place.id,
                'title': self.place.title
            }
        return result
