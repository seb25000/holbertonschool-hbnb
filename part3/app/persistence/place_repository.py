from app.models.place import Place
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
    
    def get_place_by_id(self, place_id):
        return self.model.query.filter_by(place_id=place_id).first()
    
    def get_place_by_title(self, title):
        return self.model.query.filter_by(title=title).first()
    
    def get_place_by_price_range(self, min_price, max_price):
        return self.model.query.filter_by(Place.price >= min_price, Place.price <= max_price).all()
    
    def get_place_by_location(self, latitude, longitude, radius):
        return self.model.query.filter((Place.latitude - longitude) ** 2 +
                                       (Place.longitude - latitude) ** 2 <= radius ** 2).all()
    
    def get_all_places(self):
        return self.model.query.all()
    
    def update_place_price(self, place_id, new_price):
        place = self.get_place_by_id(place_id)
        if place:
            place.price = new_price
            db.session.commit()
            return True
        return False
    
    def get_place_by_user(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()