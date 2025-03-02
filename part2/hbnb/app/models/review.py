from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.validate_text(text)
        self.validate_rating(rating)
        
        self.text = text
        self.rating = int(rating)
        self.place_id = place.id  # Stocker seulement l'ID au lieu de l'objet complet
        self.user_id = user.id    # Stocker seulement l'ID au lieu de l'objet complet
        
        # Garder des références aux objets pour faciliter l'accès
        # mais ces attributs ne seront pas sérialisés directement
        self._place = place
        self._user = user
        
        # Add this review to the place's reviews
        place.add_review(self)

    @property
    def place(self):
        """Getter for place object"""
        return self._place
    
    @property
    def user(self):
        """Getter for user object"""
        return self._user

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
        
        # Ajouter des informations minimales sur l'utilisateur
        if hasattr(self, '_user'):
            result['user'] = {
                'id': self._user.id,
                'first_name': self._user.first_name,
                'last_name': self._user.last_name,
                'email': self._user.email
            }
        
        # Ajouter des informations minimales sur le lieu
        if hasattr(self, '_place'):
            result['place'] = {
                'id': self._place.id,
                'name': self._place.name
            }
            
        return result
    