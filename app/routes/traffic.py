from flask import request, jsonify, abort
from functools import wraps
from app import app, db
from app.models import Traffic, TrafficCoordinates
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
        db.session.flush()  

        if 'geometry' in data:
            for geom_list in data['geometry']: 
                for geom in geom_list:  
                    traffic_coord = TrafficCoordinates(
                        traffic_id=traffic.id,
                        latitude=geom['latitude'],
                        longitude=geom['longitude']
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
        coords_list = [[{'latitude': coord.latitude, 'longitude': coord.longitude} for coord in data.coordinates]]
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

        coords_list = [[{'latitude': coord.latitude, 'longitude': coord.longitude} for coord in traffic_data.coordinates]]
        
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

@app.route('/traffic/clear', methods=['DELETE'])
@require_api_key
def clear_traffic():
    try:
        traffics = Traffic.query.all()
        for traffic in traffics:
            db.session.delete(traffic)
        db.session.commit()
        return jsonify({'message': 'Successfully removed all traffic records.'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Error clearing traffic records: {str(e)}'}), 500

@app.route('/traffic/<int:id>', methods=['DELETE'])
@require_api_key
def delete_traffic(id):
    traffic_data = Traffic.query.get(id)
    if traffic_data:
        try:
            TrafficCoordinates.query.filter_by(traffic_id=id).delete()
            db.session.delete(traffic_data)
            db.session.commit()
            return jsonify({'message': f'Traffic data with id {id} successfully deleted.'}), 200
        except SQLAlchemyError as e:
            db.session.rollback() 
            return jsonify({'error': f'Error deleting traffic data with id {id}: {str(e)}'}), 500
    else:
        return jsonify({'error': f'Traffic data with id {id} not found'}), 404