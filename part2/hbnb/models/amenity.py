from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name):
        """Validate amenity name"""
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")

    def update(self, data):
        """Update amenity attributes with validation"""
        if 'name' in data:
            self.validate_name(data['name'])
        
        super().update(data)
