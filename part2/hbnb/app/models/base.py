import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def to_dict(self):
        """Convert the object to a dictionary representation"""
        result = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')  # Exclude private attributes
        }
        # Convert datetime objects to ISO format strings
        for key in ['created_at', 'updated_at']:
            if key in result:
                result[key] = result[key].isoformat()
        return result 
