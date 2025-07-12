from .basemodel import BaseModel
from app import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def update(self, data):
        return super().update(data)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
