from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class to define amenities of the home to rent
    """


    def __init__(self, name):
        super().__init__()
        self.name = name


    def validate(self):
        if not self.name or len(self.name) > 50:
            raise ValueError("Name is required and must be 50 characters or less")


    def update(self, data):
        super().update(data)
        self.validate()


    def __repr__(self):
        return f"<Amenity id={self.id} name={self}"