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


class Rental(db.model):
    __tablename__ = 'rentals'

    rental_id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.vehicle_id'), nullable=False) 
    duration_days = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  

    def __repr__(self):
        return f"Rental ID: {self.rental_id} - Vehicle: {self.vehicle_id} - Duration: {self.duration_days} days"







