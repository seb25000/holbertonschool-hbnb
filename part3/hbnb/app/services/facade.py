from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from werkzeug.security import generate_password_hash, check_password_hash

class HBnBFacade:
    def __init__(self):
        # Initialisation des différents dépôts en mémoire
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # USER
    def create_user(self, user_data):
        # Créer un nouvel utilisateur et hacher le mot de passe
        user = User(**user_data)
        user.hash_password(user_data['password'])  # Hachage du mot de passe avant sauvegarde
        self.user_repo.add(user)
        return user
    
    def get_users(self):
        # Récupérer la liste de tous les utilisateurs
        return self.user_repo.get_all()

    def get_user(self, user_id):
        # Récupérer un utilisateur par son ID
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        # Récupérer un utilisateur par son email
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        # Mettre à jour un utilisateur par son ID
        self.user_repo.update(user_id, user_data)

    def verify_user_password(self, email, password):
        # Vérifier si l'email et le mot de passe sont valides
        user = self.user_repo.get_by_attribute('email', email)
        if user and user.verify_password(password):  # Vérifier le mot de passe
            return user
        return None
    
    # AMENITY
    def create_amenity(self, amenity_data):
        # Créer une nouvelle commodité
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Récupérer une commodité par son ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Récupérer toutes les commodités
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Mettre à jour une commodité
        self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE
    def create_place(self, place_data):
        # Créer un nouvel endroit, associer un utilisateur et des commodités
        user = self.user_repo.get_by_attribute('id', place_data['owner_id'])
        if not user:
            raise KeyError('Invalid input data: User not found')
        del place_data['owner_id']
        place_data['owner'] = user
        
        amenities = place_data.pop('amenities', None)
        if amenities:
            for a in amenities:
                amenity = self.get_amenity(a['id'])
                if not amenity:
                    raise KeyError('Invalid input data: Amenity not found')
        
        place = Place(**place_data)
        self.place_repo.add(place)
        user.add_place(place)
        
        if amenities:
            for amenity in amenities:
                place.add_amenity(amenity)
        return place

    def get_place(self, place_id):
        # Récupérer un endroit par son ID
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Récupérer tous les endroits
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Mettre à jour un endroit
        self.place_repo.update(place_id, place_data)

    # REVIEWS
    def create_review(self, review_data):
        # Créer une nouvelle revue
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid input data: User not found')
        del review_data['user_id']
        review_data['user'] = user
        
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid input data: Place not found')
        del review_data['place_id']
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review
        
    def get_review(self, review_id):
        # Récupérer une revue par son ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Récupérer toutes les revues
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Récupérer toutes les revues d'un endroit
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        # Mettre à jour une revue
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        # Supprimer une revue
        review = self.review_repo.get(review_id)
        user = self.user_repo.get(review.user.id)
        place = self.place_repo.get(review.place.id)

        user.delete_review(review)
        place.delete_review(review)
        self.review_repo.delete(review_id)
