#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

# Local imports
from config import app, db, api
from models import Owner,Vehicle,Rental,Feature
# Add your model imports
app = Flask(__name__)

# Configure database (assuming you have a database connection setup)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 

db = SQLAlchemy(app)


# Views go here!

@app.route('/')
def index():
    return '<h1>Backend Deluxe Motors Server</h1>'


def owner_to_dict(owner):
    return {
        'owner_id': owner.owner_id,
        'owner_name': owner.owner_name,
        'contact_info': owner.contact_info,
        'age': owner.age,
        'address': owner.address 
    } 

@app.route('/owners', methods=['GET', 'POST'])
def owners():
    if request.method == 'GET':
        owners = Owner.query.all()
        return jsonify([owner_to_dict(owner) for owner in owners])
    elif request.method == 'POST':
        data = request.get_json()  # Get data from request body
        if not data or not all(field in data for field in ['owner_name', 'contact_info', 'age', 'address']):
            return jsonify({'error': 'Missing required fields'}), 400 #bad 

        new_owner = Owner(
            owner_name=data['owner_name'],
            contact_info=data['contact_info'],
            age=data['age'],
            address=data['address']
        )
        db.session.add(new_owner)
        db.session.commit()
        return jsonify(owner_to_dict(new_owner)), 201  

@app.route('/owners/<int:owner_id>', methods=['PATCH', 'DELETE'])
def owner(owner_id):
    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing data'}), 400  #bad

        owner = Owner.query.get(owner_id)
        if not owner:
            return jsonify({'error': 'Owner not found'}), 404  # Not found

        for field, value in data.items():
            setattr(owner, field, value)  

        db.session.commit()
        return jsonify(owner_to_dict(owner))

    elif request.method == 'DELETE':
        owner = Owner.query.get(owner_id)
        if not owner:
            return jsonify({'error': 'Owner not found'}), 404  # Not found

        db.session.delete(owner)
        db.session.commit()
        return jsonify({'message': 'Owner deleted successfully'})


@app.route('/rentals', methods=['GET', 'POST'])
def rentals():
    if request.method == 'GET':
        rentals = Rental.query.all()
        return jsonify([rental.to_dict() for rental in rentals])
    elif request.method == 'POST':
        data = request.get_json()  
        if not data or not all(field in data for field in ['vehicle_id', 'duration_days', 'price']):
            return jsonify({'error': 'Missing required fields'}), 400   

    
        vehicle = Vehicle.query.get(data['vehicle_id']) 
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404  

        new_rental = Rental(
            vehicle_id=data['vehicle_id'],
            duration_days=data['duration_days'],
            price=data['price']
        )
        db.session.add(new_rental)
        db.session.commit()
        return jsonify(new_rental.to_dict()), 201  


if __name__ == '__main__':
    app.run(port=5555, debug=True)


