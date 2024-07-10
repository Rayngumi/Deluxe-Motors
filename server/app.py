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

def vehicle_to_dict(vehicle):
    return {
        'vehicle_id': vehicle.vehicle_id,
        'make': vehicle.make,
        'model': vehicle.model,
        'car_image': vehicle.car_image,
        'year': vehicle.year,
        'price': vehicle.price,
        'description': vehicle.description,
        'owner_id': vehicle.owner_id,
        'features': [feature.feature_id for feature in vehicle.features]
    }

def rental_to_dict(rental):
    return {
        'customer_name': rental.customer_name,
        'rental_id': rental.rental_id,
        'vehicle_id': rental.vehicle_id,
        'duration_days': rental.duration_days,
        'price': rental.price,
        'vehicle': vehicle_to_dict(rental.vehicle) if rental.vehicle else None
    }

def feature_to_dict(feature):
    return {
        'feature_id': feature.feature_id,
        'speed_km': feature.speed_km,
        'car_cc': feature.car_cc,
        'fuel_type': feature.fuel_type,
        'color': feature.color
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

@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    if request.method == 'GET':
        vehicles = Vehicle.query.all()
        return jsonify([vehicle_to_dict(vehicle) for vehicle in vehicles])
    elif request.method == 'POST':
        data = request.get_json()
        if not data or not all(field in data for field in ['make', 'model', 'year', 'price']):
            return jsonify({'error': 'Missing required fields'}), 400

        new_vehicle = Vehicle(
            vehicle_id=data['vehicle_id'],
            make=data['make'],
            model=data['model'],
            car_image=data.get('car_image'),  # Optional field
            year=data['year'],
            price=data['price'],
            description=data.get('description'),  # Optional field
            owner_id=data.get('owner_id')  # Optional field
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify(vehicle_to_dict(new_vehicle)), 201

@app.route('/vehicles/<int:vehicle_id>', methods=['PATCH', 'DELETE'])
def vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404

    if request.method == 'PATCH':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing data'}), 400

        for field, value in data.items():
            if field in ['vehicle_id','make', 'model', 'car_image', 'year', 'price', 'description', 'owner_id']:
                setattr(vehicle, field, value)

        db.session.commit()
        return jsonify(vehicle_to_dict(vehicle))

    elif request.method == 'DELETE':
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle deleted successfully'})

@app.route('/rentals', methods=['GET', 'POST'])
def rentals():
    if request.method == 'GET':
        rentals = Rental.query.all()
        return jsonify([rental_to_dict(rental) for rental in rentals])
    elif request.method == 'POST':
        data = request.get_json()
        if not data or not all(field in data for field in ['customer_name','vehicle_id', 'duration_days', 'price']):
            return jsonify({'error': 'Missing required fields'}), 400

        vehicle = Vehicle.query.get(data['vehicle_id'])
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404

        new_rental = Rental(
            customer_name=data['customer_name'],
            vehicle_id=data['vehicle_id'],
            duration_days=data['duration_days'],
            price=data['price']
        )
        db.session.add(new_rental)
        db.session.commit()
        return jsonify(rental_to_dict(new_rental)), 201

@app.route('/features', methods=['GET', 'POST'])
def features():
    if request.method == 'GET':
        features = Feature.query.all()
        return jsonify([feature_to_dict(feature) for feature in features])
    elif request.method == 'POST':
        data = request.get_json()
        if not data or not all(field in data for field in ['speed_km', 'car_cc', 'fuel_type', 'color']):
            return jsonify({'error': 'Missing required fields'}), 400

        new_feature = Feature(
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

if __name__ == '__main__':
    app.run(port=5555, debug=True)
