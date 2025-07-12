from .basemodel import BaseModel
from .place import Place
from .user import User
from app import db
from sqlalchemy.orm import validates


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)

    @validates("rating")
    def rating(self, value):
        super().is_between('Rating', value, 1, 6)
        self.rating = value

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id
        }
