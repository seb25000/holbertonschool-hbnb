from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        pass

    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        pass

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if user:
            self.user_repo.update(user_id, user_data)
            return self.get_user(user_id)
        return None
    