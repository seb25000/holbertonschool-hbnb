from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenities import Amenity
from app.models.places import Place
from app.models.reviews import Review
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # User
    def create_user(self, user_data):
        if self.get_user_by_email(user_data['email']):
            raise ValueError("Email already registered")
        user = User(**user_data)
        self.user_repo.add(user)
        return user


    def get_user(self, user_id):
        return self.user_repo.get(user_id)


    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    def get_all_users(self):
        return self.user_repo.get_all()


    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        user.update(user_data)
        return user

    #Amenity
    def create_amenity(self, amenity_data):
        try:
            amenity = Amenity(name=amenity_data['name'])
            self.amenity_repo.add(amenity)
            return amenity
        except ValueError as e:
            raise ValueError(f"Invalid amenity data: {e}")


    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity


    def get_all_amenities(self):
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        try:
            amenity.update(amenity_data)
        except ValueError as e:
            raise ValueError(f"Invalid update date:{e}")


    #Place
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        
        amenities = []
        for amenity_id in place_data.get('amenities',[]):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            amenities.append(amenity)

        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner,
                amenities=amenities
            )
            self.place_repo.add(place)
            return place
        except ValueError as e:
            raise ValueError(f"Invalid place data: {e}")


    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        try:
            place.update(place_data)
            if 'amenities' in place_data:
                amenities = []
                for amenity_id in place_data['amenities']:
                    amenity = self.amenity_repo.get(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity with ID {amenity_id} not found")
                    amenities.append(amenity)
                place.amenities = amenities
        except ValueError as e:
            raise ValueError (f"Invalid update data: {e}")

    #Reviews
    def create_review(self, review_data):
        """Create a new review"""
        if 'user_id' not in review_data or 'place_id' not in review_data or 'text' not in review_data or 'rating' not in review_data:
            raise ValueError("Missing required fields")
        
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")
        
        rating = review_data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        review = Review(
            text=review_data['text'],
            rating=rating,
            user=user,
            place=place
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review


    def get_all_reviews(self):
        return self.review_repo.get_all()


    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews


    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)

        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or rating <1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")

        review.update(review_data)


    def delete_review(self, review_id):
        review = self.get_review(review_id)
        self.review_repo.delete(review_id)