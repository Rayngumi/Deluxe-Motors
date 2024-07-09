from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

class Owner(db.model):
    __tablename__ = 'owners'

    owner_id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Owner(id={self.owner_id}, name='{self.owner_name}', age={self.age})"


class Feature:
    pass


class Vehicle:
    pass


class Rental(db.model):
    __tablename__ = 'rentals'

    rental_id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.vehicle_id'), nullable=False) 
    duration_days = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  

    def __repr__(self):
        return f"Rental ID: {self.rental_id} - Vehicle: {self.vehicle_id} - Duration: {self.duration_days} days"







