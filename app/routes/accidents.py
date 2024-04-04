from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from app import db
from app.models import Accident, AccidentCoordinates
from config import Config

accidents_bp = Blueprint('accidents', __name__)

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

@accidents_bp.route('', methods=['POST'])
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
        db.session.flush()  
        
        if 'geometry' in data:
            for geom_list in data['geometry']: 
                for geom in geom_list:  
                    acc_coord = AccidentCoordinates(
                        accident_id=accident.id,
                        latitude=geom['latitude'],
                        longitude=geom['longitude']
                    )
                    db.session.add(acc_coord)

        db.session.commit()
        message = "Accident record added successfully."
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add accident record: ' + str(e)}), 500

    return jsonify({'message': message}), 201

@accidents_bp.route('', methods=['GET'])
@require_api_key
def get_accidents():
    try:
        accidents = Accident.query.all()
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error fetching accidents from database: {str(e)}'}), 500

    accidents_list = []
    for accident in accidents:
        coords_list = [[{'latitude': coord.latitude, 'longitude': coord.longitude} for coord in accident.coordinates]]
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

@accidents_bp.route('/<int:id>', methods=['GET'])
@require_api_key
def get_accident(id):
    try:
        accident = Accident.query.get(id)
        if not accident:
            return jsonify({'error': f'Accident with id {id} not found'}), 404

        coords_list = [[{'latitude': coord.latitude, 'longitude': coord.longitude} for coord in accident.coordinates]]
        
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

@accidents_bp.route('/clear', methods=['DELETE'])
@require_api_key
def clear_accidents():
    try:
        num_rows_deleted = db.session.query(Accident).delete()
        db.session.commit()
        return jsonify({'message': f'Successfully removed {num_rows_deleted} accident records.'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Error clearing accident records: {str(e)}'}), 500

@accidents_bp.route('/<int:id>', methods=['DELETE'])
@require_api_key
def delete_accident(id):
    accident = Accident.query.get(id)
    if accident:
        try:
            AccidentCoordinates.query.filter_by(accident_id=id).delete()
            db.session.delete(accident)
            db.session.commit()
            return jsonify({'message': f'Accident with id {id} successfully deleted.'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()  
            return jsonify({'error': f'Error deleting accident with id {id}: {str(e)}'}), 500
    else:
        return jsonify({'error': f'Accident with id {id} not found'}), 404
