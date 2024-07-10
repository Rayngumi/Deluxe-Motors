#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, jsonify
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import Owner, Vehicle, Rental, Feature, VehicleFeatures

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
        data = request.get_json()
        if not data or not all(field in data for field in ['owner_name', 'contact_info', 'age', 'address']):
            return jsonify({'error': 'Missing required fields'}), 400

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
    owner = Owner.query.get(owner_id)
    if not owner:
        return jsonify({'error': 'Owner not found'}), 404

    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing data'}), 400

        for field, value in data.items():
            if field in ['owner_name', 'contact_info', 'age', 'address']:
                setattr(owner, field, value)

        db.session.commit()
        return jsonify(owner_to_dict(owner))

    elif request.method == 'DELETE':
        db.session.delete(owner)
        db.session.commit()
        return jsonify({'message': 'Owner deleted successfully'})

@app.route('/rentals', methods=['GET', 'POST'])
def rentals():
    def rental_to_dict(rental):
        return {
            'rental_id': rental.rental_id,
            'vehicle_id': rental.vehicle_id,
            'duration_days': rental.duration_days,
            'price': rental.price
        }

    if request.method == 'GET':
        rentals = Rental.query.all()
        return jsonify([rental_to_dict(rental) for rental in rentals])
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
        return jsonify(rental_to_dict(new_rental)), 201

def feature_to_dict(feature):
    return {
        'feature_id': feature.feature_id,
        'speed_km': feature.speed_km,
        'car_cc': feature.car_cc,
        'fuel_type': feature.fuel_type,
        'color': feature.color
    }

@app.route('/features', methods=['GET', 'POST'])
def features():
    if request.method == 'GET':
        features = Feature.query.all()
        return jsonify([feature_to_dict(feature) for feature in features])
    elif request.method == 'POST':
        data = request.get_json()
        if not data or not all(field in data for field in ['feature_id', 'speed_km', 'car_cc', 'fuel_type', 'color']):
            return jsonify({'error': 'Missing required fields'}), 400

        new_feature = Feature(
            feature_id=data['feature_id'],
            speed_km=data['speed_km'],
            car_cc=data['car_cc'],
            fuel_type=data['fuel_type'],
            color=data['color']
        )
        db.session.add(new_feature)
        db.session.commit()
        return jsonify(feature_to_dict(new_feature)), 201

@app.route('/features/<int:feature_id>', methods=['PATCH', 'DELETE'])
def feature(feature_id):
    feature = Feature.query.get(feature_id)
    if not feature:
        return jsonify({'error': 'Feature not found'}), 404

    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing data'}), 400

        for field, value in data.items():
            if field in ['speed_km', 'car_cc', 'fuel_type', 'color']:
                setattr(feature, field, value)

        db.session.commit()
        return jsonify(feature_to_dict(feature))

    elif request.method == 'DELETE':
        db.session.delete(feature)
        db.session.commit()
        return jsonify({'message': 'Feature deleted successfully'})

@app.route('/vehicles/<int:vehicle_id>/features', methods=['POST'])
def add_feature_to_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404

    data = request.get_json()
    if not data or not all(field in data for field in ['feature_id']):
        return jsonify({'error': 'Missing required fields'}), 400

    feature = Feature.query.get(data['feature_id'])
    if not feature:
        return jsonify({'error': 'Feature not found'}), 404

    vehicle.features.append(feature)
    db.session.commit()
    return jsonify(feature_to_dict(feature))

if __name__ == '__main__':
    app.run(port=5555, debug=True)
