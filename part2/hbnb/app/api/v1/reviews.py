from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the user model for nested responses
user_model = api.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address')
})

# Define the place model for nested responses
place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place')
})

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Define the review response model
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user': fields.Nested(user_model, description='User who wrote the review'),
    'place': fields.Nested(place_model, description='Place being reviewed'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created', review_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or place not found')
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """Register a new review"""
        try:
            new_review = facade.create_review(api.payload)
            return new_review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_reviews')
    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews]

@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.response(200, 'Review details retrieved successfully', review_response_model)
    @api.response(404, 'Review not found')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review.to_dict()

    @api.doc('update_review')
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully', review_response_model)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_response_model)
    def put(self, review_id):
        """Update a review's information"""
        try:
            review = facade.update_review(review_id, api.payload)
            if not review:
                api.abort(404, 'Review not found')
            return review.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}
        api.abort(404, 'Review not found')

@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_list_with(review_response_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews]
        except ValueError:
            api.abort(404, 'Place not found')
