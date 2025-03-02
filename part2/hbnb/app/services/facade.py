from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.services.validation import Validator, ValidationError
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HBnBFacade:
    """
    Facade for the HBnB application that manages all operations on entities.
    This class serves as an intermediary between API controllers and repositories.
    """
    
    def __init__(self):
        """Initialize repositories for each entity type."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        logger.info("HBnBFacade initialized with in-memory repositories")

    # User methods
    def get_all_users(self):
        """Retrieve all users.
        
        Returns:
            list: List of all users
        """
        logger.info("Fetching all users")
        return self.user_repo.get_all()

    def get_user(self, user_id):
        """Retrieve a user by ID.
        
        Args:
            user_id (str): ID of the user to retrieve
            
        Returns:
            User: The user corresponding to the ID or None if it doesn't exist
        """
        logger.info(f"Fetching user with ID: {user_id}")
        return self.user_repo.get(user_id)

    def create_user(self, user_data):
        """Create a new user.
        
        Args:
            user_data (dict): User data (first_name, last_name, email, password)
            
        Returns:
            User: The created user
            
        Raises:
            ValidationError: If the data is invalid
        """
        try:
            logger.info(f"Creating new user with data: {user_data}")
            
            # Validate required fields
            Validator.validate_required_fields(user_data, ['first_name', 'last_name', 'email'])
            
            # Validate individual fields
            Validator.validate_string(user_data['first_name'], 'first_name', max_length=50)
            Validator.validate_string(user_data['last_name'], 'last_name', max_length=50)
            Validator.validate_email(user_data['email'])
            
            # Validate password if provided
            if 'password' in user_data and user_data['password']:
                Validator.validate_password(user_data['password'])
            
            # Create user
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data.get('password'),
                is_admin=user_data.get('is_admin', False)
            )
            
            # Add to repository
            self.user_repo.add(user)
            logger.info(f"User created successfully with ID: {user.id}")
            return user
        except ValidationError as e:
            logger.error(f"Validation error creating user: {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

    def update_user(self, user_id, user_data):
        """Update an existing user.
        
        Args:
            user_id (str): ID of the user to update
            user_data (dict): New user data
            
        Returns:
            User: The updated user or None if it doesn't exist
            
        Raises:
            ValueError: If the data is invalid
        """
        try:
            logger.info(f"Updating user with ID: {user_id}")
            user = self.user_repo.get(user_id)
            if not user:
                logger.warning(f"User with ID {user_id} not found")
                return None
            
            user.update(user_data)
            logger.info(f"User with ID {user_id} updated successfully")
            return user
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise

    def delete_user(self, user_id):
        """Delete a user.
        
        Args:
            user_id (str): ID of the user to delete
            
        Returns:
            bool: True if the user was deleted, False otherwise
        """
        logger.info(f"Deleting user with ID: {user_id}")
        user = self.user_repo.get(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            return False
        
        self.user_repo.delete(user_id)
        logger.info(f"User with ID {user_id} deleted successfully")
        return True

    # Place methods
    def get_all_places(self):
        """Retrieve all places.
        
        Returns:
            list: List of all places
        """
        logger.info("Fetching all places")
        return self.place_repo.get_all()

    def get_place(self, place_id):
        """Retrieve a place by ID.
        
        Args:
            place_id (str): ID of the place to retrieve
            
        Returns:
            Place: The place corresponding to the ID or None if it doesn't exist
        """
        logger.info(f"Fetching place with ID: {place_id}")
        return self.place_repo.get(place_id)

    def create_place(self, place_data):
        """Create a new place.
        
        Args:
            place_data (dict): Place data
            
        Returns:
            Place: The created place
            
        Raises:
            ValidationError: If the data is invalid
            ValueError: If the user doesn't exist
        """
        try:
            logger.info(f"Creating new place with data: {place_data}")
            
            # Validate required fields
            required_fields = ['name', 'description', 'number_rooms', 'number_bathrooms', 
                              'max_guest', 'price_by_night', 'latitude', 'longitude', 'user_id']
            Validator.validate_required_fields(place_data, required_fields)
            
            # Validate individual fields
            Validator.validate_string(place_data['name'], 'name', max_length=100)
            Validator.validate_string(place_data['description'], 'description', min_length=0)
            Validator.validate_number(place_data['number_rooms'], 'number_rooms', min_value=0, integer=True)
            Validator.validate_number(place_data['number_bathrooms'], 'number_bathrooms', min_value=0, integer=True)
            Validator.validate_number(place_data['max_guest'], 'max_guest', min_value=0, integer=True)
            Validator.validate_number(place_data['price_by_night'], 'price_by_night', min_value=0)
            Validator.validate_coordinates(place_data['latitude'], place_data['longitude'])
            
            # Check if user exists
            user = self.user_repo.get(place_data['user_id'])
            if not user:
                raise ValueError(f"User with ID {place_data['user_id']} not found")
            
            # Create place
            place = Place(
                name=place_data['name'],
                description=place_data['description'],
                number_rooms=place_data['number_rooms'],
                number_bathrooms=place_data['number_bathrooms'],
                max_guest=place_data['max_guest'],
                price_by_night=place_data['price_by_night'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                user=user
            )
            
            # Add amenities if present
            if 'amenity_ids' in place_data and place_data['amenity_ids']:
                for amenity_id in place_data['amenity_ids']:
                    amenity = self.amenity_repo.get(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)
            
            # Add to repository
            self.place_repo.add(place)
            
            logger.info(f"Place created successfully with ID: {place.id}")
            return place
        except ValidationError as e:
            logger.error(f"Validation error creating place: {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Error creating place: {str(e)}")
            raise

    def update_place(self, place_id, place_data):
        """Update an existing place.
        
        Args:
            place_id (str): ID of the place to update
            place_data (dict): New place data
            
        Returns:
            Place: The updated place or None if it doesn't exist
            
        Raises:
            ValueError: If the data is invalid
        """
        try:
            logger.info(f"Updating place with ID: {place_id}")
            place = self.place_repo.get(place_id)
            if not place:
                logger.warning(f"Place with ID {place_id} not found")
                return None
            
            # Update amenities if present
            if 'amenity_ids' in place_data:
                # Reset amenities
                place.amenities = []
                
                # Add new amenities
                for amenity_id in place_data['amenity_ids']:
                    amenity = self.amenity_repo.get(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)
                
                # Remove key to avoid processing by update()
                del place_data['amenity_ids']
            
            place.update(place_data)
            logger.info(f"Place with ID {place_id} updated successfully")
            return place
        except Exception as e:
            logger.error(f"Error updating place: {str(e)}")
            raise

    def delete_place(self, place_id):
        """Delete a place.
        
        Args:
            place_id (str): ID of the place to delete
            
        Returns:
            bool: True if the place was deleted, False otherwise
        """
        logger.info(f"Deleting place with ID: {place_id}")
        place = self.place_repo.get(place_id)
        if not place:
            logger.warning(f"Place with ID {place_id} not found")
            return False
        
        self.place_repo.delete(place_id)
        logger.info(f"Place with ID {place_id} deleted successfully")
        return True

    # Review methods
    def get_all_reviews(self):
        """Retrieve all reviews.
        
        Returns:
            list: List of all reviews
        """
        logger.info("Fetching all reviews")
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place.
        
        Args:
            place_id (str): ID of the place
            
        Returns:
            list: List of reviews for the place
        """
        logger.info(f"Fetching reviews for place with ID: {place_id}")
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]

    def get_review(self, review_id):
        """Retrieve a review by ID.
        
        Args:
            review_id (str): ID of the review to retrieve
            
        Returns:
            Review: The review corresponding to the ID or None if it doesn't exist
        """
        logger.info(f"Fetching review with ID: {review_id}")
        return self.review_repo.get(review_id)

    def create_review(self, review_data):
        """Create a new review.
        
        Args:
            review_data (dict): Review data
            
        Returns:
            Review: The created review
            
        Raises:
            ValidationError: If the data is invalid
            ValueError: If the user or place doesn't exist
        """
        try:
            logger.info(f"Creating new review with data: {review_data}")
            
            # Validate required fields
            required_fields = ['text', 'rating', 'user_id', 'place_id']
            Validator.validate_required_fields(review_data, required_fields)
            
            # Validate individual fields
            Validator.validate_string(review_data['text'], 'text')
            Validator.validate_number(review_data['rating'], 'rating', min_value=1, max_value=5, integer=True)
            
            # Check if user exists
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError(f"User with ID {review_data['user_id']} not found")
            
            # Check if place exists
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError(f"Place with ID {review_data['place_id']} not found")
            
            # Create review
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                user=user,
                place=place
            )
            
            # Add to repository
            self.review_repo.add(review)
            
            logger.info(f"Review created successfully with ID: {review.id}")
            return review
        except ValidationError as e:
            logger.error(f"Validation error creating review: {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Error creating review: {str(e)}")
            raise

    def update_review(self, review_id, review_data):
        """Update an existing review.
        
        Args:
            review_id (str): ID of the review to update
            review_data (dict): New review data
            
        Returns:
            Review: The updated review or None if it doesn't exist
            
        Raises:
            ValueError: If the data is invalid
        """
        try:
            logger.info(f"Updating review with ID: {review_id}")
            review = self.review_repo.get(review_id)
            if not review:
                logger.warning(f"Review with ID {review_id} not found")
                return None
            
            review.update(review_data)
            logger.info(f"Review with ID {review_id} updated successfully")
            return review
        except Exception as e:
            logger.error(f"Error updating review: {str(e)}")
            raise

    def delete_review(self, review_id):
        """Delete a review.
        
        Args:
            review_id (str): ID of the review to delete
            
        Returns:
            bool: True if the review was deleted, False otherwise
        """
        logger.info(f"Deleting review with ID: {review_id}")
        review = self.review_repo.get(review_id)
        if not review:
            logger.warning(f"Review with ID {review_id} not found")
            return False
        
        self.review_repo.delete(review_id)
        logger.info(f"Review with ID {review_id} deleted successfully")
        return True

    # Amenity methods
    def get_all_amenities(self):
        """Retrieve all amenities.
        
        Returns:
            list: List of all amenities
        """
        logger.info("Fetching all amenities")
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID.
        
        Args:
            amenity_id (str): ID of the amenity to retrieve
            
        Returns:
            Amenity: The amenity corresponding to the ID or None if it doesn't exist
        """
        logger.info(f"Fetching amenity with ID: {amenity_id}")
        return self.amenity_repo.get(amenity_id)

    def create_amenity(self, amenity_data):
        """Create a new amenity.
        
        Args:
            amenity_data (dict): Amenity data
            
        Returns:
            Amenity: The created amenity
            
        Raises:
            ValidationError: If the data is invalid
        """
        try:
            logger.info(f"Creating new amenity with data: {amenity_data}")
            
            # Validate required fields
            Validator.validate_required_fields(amenity_data, ['name'])
            
            # Validate individual fields
            Validator.validate_string(amenity_data['name'], 'name', max_length=50)
            
            # Create amenity
            amenity = Amenity(name=amenity_data['name'])
            
            # Add to repository
            self.amenity_repo.add(amenity)
            
            logger.info(f"Amenity created successfully with ID: {amenity.id}")
            return amenity
        except ValidationError as e:
            logger.error(f"Validation error creating amenity: {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Error creating amenity: {str(e)}")
            raise

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity.
        
        Args:
            amenity_id (str): ID of the amenity to update
            amenity_data (dict): New amenity data
            
        Returns:
            Amenity: The updated amenity or None if it doesn't exist
            
        Raises:
            ValueError: If the data is invalid
        """
        try:
            logger.info(f"Updating amenity with ID: {amenity_id}")
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                logger.warning(f"Amenity with ID {amenity_id} not found")
                return None
            
            amenity.update(amenity_data)
            logger.info(f"Amenity with ID {amenity_id} updated successfully")
            return amenity
        except Exception as e:
            logger.error(f"Error updating amenity: {str(e)}")
            raise

    def delete_amenity(self, amenity_id):
        """Delete an amenity.
        
        Args:
            amenity_id (str): ID of the amenity to delete
            
        Returns:
            bool: True if the amenity was deleted, False otherwise
        """
        logger.info(f"Deleting amenity with ID: {amenity_id}")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            logger.warning(f"Amenity with ID {amenity_id} not found")
            return False
        
        self.amenity_repo.delete(amenity_id)
        logger.info(f"Amenity with ID {amenity_id} deleted successfully")
        return True