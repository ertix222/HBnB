from app.persistence.repository import SQLAlchemyRepository

from app.services.model_repositories.user_repo import UserRepository

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # USER
    def create_user(self, user_data):
        if self.user_repo.number_of_users() == 0:
            user_data["is_admin"] = True
        user = User(**user_data)
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE
    def create_place(self, place_data, owner_id):
        user = self.user_repo.get_by_attribute('id', owner_id)
        if not user:
            raise KeyError('Invalid input data')
        place_data['owner'] = user
        amenities = place_data.pop('amenities', None)
        if amenities:
            for a in amenities:
                amenity = self.get_amenity(a['id'])
                if not amenity:
                    raise KeyError('Invalid input data')
        place = Place(**place_data)
        self.place_repo.add(place)
        user.add_place(place)
        if amenities:
            for amenity in amenities:
                place.add_amenity(amenity)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)

        owner = self.user_repo.get(place.owner.id)

        owner.delete_place(place)

        for i in place.reviews:
            owner.delete_review(i.id)
            self.review_repo.delete(i.id)
        self.place_repo.delete(place_id)

    # REVIEWS
    def create_review(self, review_data, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise KeyError('Invalid input data')
        review_data['user'] = user

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid input data')
        del review_data['place_id']
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)

        user = self.user_repo.get(review.user.id)
        place = self.place_repo.get(review.place.id)

        user.delete_review(review)
        place.delete_review(review)
        self.review_repo.delete(review_id)
