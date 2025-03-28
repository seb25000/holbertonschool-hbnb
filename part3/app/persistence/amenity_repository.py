from app.models.amenity import Amenity
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
    
    def get_amenity_by_id(self, amenity_id):
        return self.model.query.filter_by(amenity_id=amenity_id).first()
    
    def get_amenity_by_name(self, name):
        return self.model.query.filter_by(name=name).all()
    
    def get_all_amenities(self):
        return self.model.query.all()
    
    def update_amenity_name(self, amenity_id, new_name):
        amenity = self.get_amenity_by_id(amenity_id)
        if amenity:
            amenity.name = new_name
            db.session.commit()
            return True
        return False
    
    def create_amenity(self, name):
        new_amenity = Amenity(name=name)
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity
    
    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity_by_id(amenity_id)
        if amenity:
            db.session.delete(amenity)
            db.session.commit()
            return True
        return False
    