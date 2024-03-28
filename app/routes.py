from flask import request, jsonify, abort
from functools import wraps
from app import app, db
from app.models import Accident, AccidentCoordinates, Traffic, TrafficCoordinates
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from config import Config

# API Key verification decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'API-Key' not in request.headers:
            abort(401, description='API key is missing.')
        elif request.headers['API-Key'] != Config.API_KEY:
            abort(401, description='Invalid API key.')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/accidents', methods=['POST'])
@require_api_key
def add_accident():
    data = request.get_json()
    try:
        accident = Accident(
            timestamp=datetime.fromisoformat(data['timestamp']),
            accident_type=data['accident_type'],
            severity=data['severity'],
            participants=data['participants'],
            weather_conditions=data.get('weather_conditions', None),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        db.session.add(accident)
        db.session.flush()  # Flush to get the accident id before committing

        if 'geometry' in data:
            for geom in data['geometry'][0]:
                acc_coord = AccidentCoordinates(
                    accident_id=accident.id,
                    geometry=geom
                )
                db.session.add(acc_coord)

        db.session.commit()
        message = "Accident record added successfully."
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add accident record: ' + str(e)}), 500

    return jsonify({'message': message}), 201

@app.route('/accidents', methods=['GET'])
@require_api_key
def get_accidents():
    try:
        accidents = Accident.query.all()
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching accidents from database: {str(e)}'}), 500

    accidents_list = []
    for accident in accidents:
        coords_list = [coord.geometry for coord in accident.coordinates]
        accidents_list.append({
            'id': accident.id,
            'timestamp': accident.timestamp.isoformat(),
            'accidentType': accident.accident_type,
            'severity': accident.severity,
            'participants': accident.participants,
            'weatherconditions': accident.weather_conditions,
            'latitude': accident.latitude,
            'longitude': accident.longitude,
            'geometry': coords_list
        })

    return jsonify(accidents_list)

@app.route('/accidents/<int:id>', methods=['GET'])
@require_api_key
def get_accident(id):
    try:
        accident = Accident.query.get(id)
        if not accident:
            return jsonify({'error': f'Accident with id {id} not found'}), 404

        coords_list = [coord.geometry for coord in accident.coordinates]

        accident_data = {
            'id': accident.id,
            'timestamp': accident.timestamp.isoformat(),
            'accidentType': accident.accident_type,
            'severity': accident.severity,
            'participants': accident.participants,
            'weatherconditions': accident.weather_conditions,
            'latitude': accident.latitude,
            'longitude': accident.longitude,
            'geometry': coords_list
        }

    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching accident with id {id} from database: {str(e)}'}), 500

    return jsonify(accident_data)

# traffic
@app.route('/traffic', methods=['POST'])
@require_api_key
def add_traffic():
    data = request.get_json()
    try:
        traffic = Traffic(
            timestamp=datetime.fromisoformat(data['timestamp']),
            volume=data['volume'],
            average_speed=data['averageSpeed'],
            congestion_level=data.get('congestionLevel', None),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        db.session.add(traffic)
        db.session.flush()  # Flush to get the traffic id before committing

        if 'geometry' in data:
            for geom in data['geometry'][0]:
                traffic_coord = TrafficCoordinates(
                    traffic_id=traffic.id,
                    geometry=geom
                )
                db.session.add(traffic_coord)

        db.session.commit()
        message = "Traffic record added successfully."
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add traffic record: ' + str(e)}), 500

    return jsonify({'message': message}), 201

@app.route('/traffic', methods=['GET'])
@require_api_key
def get_traffic():
    try:
        traffic_data = Traffic.query.all()
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching traffic data from database: {str(e)}'}), 500

    traffic_list = []
    for data in traffic_data:
        coords_list = [coord.geometry for coord in data.coordinates]
        traffic_list.append({
            'id': data.id,
            'timestamp': data.timestamp.isoformat(),
            'volume': data.volume,
            'averageSpeed': data.average_speed,
            'congestionLevel': data.congestion_level,
            'latitude': data.latitude,
            'longitude': data.longitude,
            'geometry': coords_list
        })

    return jsonify(traffic_list)

@app.route('/traffic/<int:id>', methods=['GET'])
@require_api_key
def get_traffic_data(id):
    try:
        traffic_data = Traffic.query.get(id)
        if not traffic_data:
            return jsonify({'error': f'Traffic data with id {id} not found'}), 404

        coords_list = [coord.geometry for coord in traffic_data.coordinates]

        traffic_details = {
            'id': traffic_data.id,
            'timestamp': traffic_data.timestamp.isoformat(),
            'volume': traffic_data.volume,
            'averageSpeed': traffic_data.average_speed,
            'congestionLevel': traffic_data.congestion_level,
            'latitude': traffic_data.latitude,
            'longitude': traffic_data.longitude,
            'geometry': coords_list
        }

    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching traffic data with id {id} from database: {str(e)}'}), 500

    return jsonify(traffic_details)
