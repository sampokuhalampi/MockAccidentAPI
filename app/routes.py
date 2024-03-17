from flask import request, jsonify
from app import app, db
from app.models import Accident, Traffic
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

@app.route('/accidents', methods=['GET'])
def get_accidents():
    try:
        accidents = Accident.query.all()
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching accidents from database: {str(e)}'}), 500

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
    try:
        accident = Accident.query.get(id)
        if accident is None:
            return jsonify({'error': f'Accident with id {id} not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching accident with id {id} from database: {str(e)}'}), 500

    return jsonify({
        'id': accident.id,
        'location': {'latitude': accident.latitude, 'longitude': accident.longitude},
        'timestamp': accident.timestamp.isoformat(),
        'accidentType': accident.accident_type,
        'severity': accident.severity,
        'participants': accident.participants,
        'weatherconditions': accident.weather_conditions
    })

@app.route('/accidents', methods=['POST'])
def add_accident():
    data = request.get_json()
    try:
        accident = Accident(
            latitude=data['latitude'],
            longitude=data['longitude'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            accident_type=data['accident_type'],
            severity=data['severity'],
            participants=data['participants'],
            weather_conditions=data['weather_conditions']
        )
        db.session.add(accident)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Failed to add accident record'}), 500

    return jsonify({'message': 'Accident record added successfully'}), 201

# traffic
@app.route('/traffic', methods=['GET'])
def get_traffic():
    try:
        traffic_data = Traffic.query.all()
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching traffic data from database: {str(e)}'}), 500

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
    try:
        traffic_data = Traffic.query.get(id)
        if traffic_data is None:
            return jsonify({'error': f'Traffic data with id {id} not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching traffic data with id {id} from database: {str(e)}'}), 500

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
    try:
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
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Failed to add traffic data'}), 500

    return jsonify({'message': 'Traffic data added successfully'}), 201
