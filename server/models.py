from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

class Owner:
    pass


class Feature(db.Model):
    __tablename__ = 'features'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    car_cc = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String, nullable=False)
    car = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"<Feature(id={self.id}, name={self.name}, car_cc={self.car_cc}, fuel_type={self.fuel_type})>"


class Vehicle:
    pass


class Rental:
    pass






