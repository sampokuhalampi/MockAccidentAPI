from app import db
from datetime import datetime

class Accident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    accident_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    weather_conditions = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    coordinates = db.relationship('AccidentCoordinates', backref='accident', lazy=True)

    def __repr__(self):
        return f'<Accident {self.id} - {self.accident_type}, Severity: {self.severity}>'

class AccidentCoordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accident_id = db.Column(db.Integer, db.ForeignKey('accident.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<AccidentCoordinate {self.id} - Latitude: {self.latitude}, Longitude: {self.longitude}>'

class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    volume = db.Column(db.Integer, nullable=False)
    average_speed = db.Column(db.Float, nullable=False)
    congestion_level = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    coordinates = db.relationship('TrafficCoordinates', backref='traffic', lazy=True)

    def __repr__(self):
        return f'<Traffic {self.id} - Volume: {self.volume}, Avg Speed: {self.average_speed}km/h, Congestion: {self.congestion_level}>'

class TrafficCoordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    traffic_id = db.Column(db.Integer, db.ForeignKey('traffic.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<TrafficCoordinate {self.id} - Latitude: {self.latitude}, Longitude: {self.longitude}>'
