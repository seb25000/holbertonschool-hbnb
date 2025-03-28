from app.models.review import Review
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
    
    def get_review_by_id(self, review_id):
        return self.model.query.filter_by(review_id=review_id).first()
    
    def get_review_by_text(self, text):
        return self.model.query.filter_by(text=text).first()
    
    def get_review_by_rating(self, rating):
        return self.model.query.filter_by(rating=rating).all()
    
    def get_all_reviews(self):
        return self.model.query.all()
    
    def update_review_text(self, review_id, new_text):
        review = self.get_review_by_id(review_id)
        if review:
            review.text = new_text
            db.session.commit()
            return True
        return False
    
    def update_review_rating(self, review_id, new_rating):
        review = self.get_review_by_rating(review_id)
        if review:
            review.rating = new_rating
            db.session.commit()
            return True
        return False
    
    def delete_review(self, review_id):
        review = self.get_review_by_id(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False
    
    def create_review(self, text, rating, user_id):
        new_review = Review(text=text, rating=rating, user_id=user_id)
        db.session.add(new_review)
        db.session.commit()
        return new_review
    
    def get_review_by_user(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()