from app.models.base_model import BaseModel
from app.models.user import User
from app.models.places import Place


class Review(BaseModel):
    """
    Review class to put review on a place, with text, note, place and user.
    """
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user


    def validate(self):
        if not self.text:
            raise ValueError("Review text is required")
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")


    def update(self, data):
        super().update(data)
        self.validate()


    def __repr__(self):
        return f"<Review id={self.id} rating={self.rating}>"