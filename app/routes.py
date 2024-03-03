from flask import request, jsonify
from app import app, db
from app.models import Accident, Traffic
from datetime import datetime
import json

@app.route('/accidents', methods=['GET'])
def get_accidents():
    accidents = Accident.query.all()
    return jsonify([{
        'id': accident.id,
        'location': {'latitude': accident.latitude, 'longitude': accident.longitude},
        'timestamp': accident.timestamp.isoformat(),
        'accidentType': accident.accident_type,
        'severity': accident.severity,
        'participants': accident.participants,
        'weatherConditions': accident.weather_conditions
    } for accident in accidents])

@app.route('/accidents/<int:id>', methods=['GET'])
def get_accident(id):
    accident = Accident.query.get_or_404(id)
    return jsonify({
        'id': accident.id,
        'location': {'latitude': accident.latitude, 'longitude': accident.longitude},
        'timestamp': accident.timestamp.isoformat(),
        'accidentType': accident.accident_type,
        'severity': accident.severity,
        'participants': accident.participants,
        'weatherConditions': accident.weather_conditions
    })

@app.route('/accidents', methods=['POST'])
def add_accident():
    data = request.get_json()
    accident = Accident(
        latitude=data['latitude'],
        longitude=data['longitude'],
        timestamp=datetime.fromisoformat(data['timestamp']),
        accident_type=data['accident_type'],
        severity=data['severity'],
        participants=data['participants'],
        weather_conditions=data['weatheronditions']
    )
    db.session.add(accident)
    db.session.commit()
    return jsonify({'message': 'Accident record added successfully'}), 201


# traffic
@app.route('/traffic', methods=['GET'])
def get_traffic():
    traffic_data = Traffic.query.all()
    return jsonify([{
        'id': data.id,
        'location': {'latitude': data.latitude, 'longitude': data.longitude},
        'timestamp': data.timestamp.isoformat(),
        'volume': data.volume,
        'averageSpeed': data.average_speed,
        'congestionLevel': data.congestion_level
    } for data in traffic_data])

@app.route('/traffic/<int:id>', methods=['GET'])
def get_traffic_data(id):
    traffic_data = Traffic.query.get_or_404(id)
    return jsonify({
        'id': traffic_data.id,
        'location': {'latitude': traffic_data.latitude, 'longitude': traffic_data.longitude},
        'timestamp': traffic_data.timestamp.isoformat(),
        'volume': traffic_data.volume,
        'averageSpeed': traffic_data.average_speed,
        'congestionLevel': traffic_data.congestion_level
    })

@app.route('/traffic', methods=['POST'])
def add_traffic():
    data = request.get_json()
    traffic = Traffic(
        latitude=data['latitude'],
        longitude=data['longitude'],
        timestamp=datetime.fromisoformat(data['timestamp']),
        volume=data['volume'],
        average_speed=data['averageSpeed'],
        congestion_level=data.get('congestionLevel')  # Optional field
    )
    db.session.add(traffic)
    db.session.commit()
    return jsonify({'message': 'Traffic data added successfully'}), 201
