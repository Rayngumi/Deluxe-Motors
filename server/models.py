from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

class Owner:
    pass


class Feature:
    pass


class Vehicle:
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(128), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    car_image = db.Column(db.String(128), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return f'<Vehicle {self.id} {self.make} {self.model}>'


class Rental:
    pass






