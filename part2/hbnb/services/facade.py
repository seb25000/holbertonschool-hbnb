from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user"""
        # Check if email already exists
        if 'email' in user_data:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user:
                raise ValueError('Email already registered')
        
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information"""
        user = self.get_user(user_id)
        if user:
            # Check email uniqueness if email is being updated
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = self.get_user_by_email(user_data['email'])
                if existing_user:
                    raise ValueError('Email already registered')
            user.update(user_data)
        return user

    # Place-related methods
    def create_place(self, place_data):
        """Create a new place"""
        # Get the owner
        owner_id = place_data.pop('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError('Owner not found')

        # Get amenities if provided
        amenity_ids = place_data.pop('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f'Amenity with ID {amenity_id} not found')
            amenities.append(amenity)

        # Create the place
        place = Place(owner=owner, **place_data)
        
        # Add amenities
        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information"""
        place = self.get_place(place_id)
        if not place:
            return None

        # Handle amenities update if provided
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            # Clear current amenities
            place.amenities.clear()
            # Add new amenities
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f'Amenity with ID {amenity_id} not found')
                place.add_amenity(amenity)

        # Handle owner update if provided
        if 'owner_id' in place_data:
            owner_id = place_data.pop('owner_id')
            owner = self.get_user(owner_id)
            if not owner:
                raise ValueError('Owner not found')
            place_data['owner'] = owner

        place.update(place_data)
        return place

    # Amenity-related methods
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Get an amenity by name"""
        return self.amenity_repo.get_by_attribute('name', name)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information"""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity

    # Review-related methods
    def create_review(self, review_data):
        """Create a new review"""
        # Get the user and place
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')
        
        user = self.get_user(user_id)
        if not user:
            raise ValueError('User not found')
            
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')

        # Create the review
        review = Review(user=user, place=place, **review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update a review's information"""
        review = self.get_review(review_id)
        if review:
            review.update(review_data)
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.get_review(review_id)
        if review:
            # Remove the review from the place's reviews list
            review.place.reviews.remove(review)
            # Delete from repository
            self.review_repo.delete(review_id)
            return True
        return False
