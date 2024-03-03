from app import db
from datetime import datetime

class Accident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    accident_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    weather_conditions = db.Column(db.String(100))

    def __repr__(self):
        return f'<Accident {self.id} - {self.accident_type}>'

class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    volume = db.Column(db.Integer, nullable=False, comment="Liikenteen määrä, esim. ajoneuvot tunnissa")
    average_speed = db.Column(db.Float, nullable=False, comment="Keskinopeus alueella km/h")
    congestion_level = db.Column(db.String(50), nullable=True, comment="Ruuhkan taso, esim. kevyt, kohtalainen, raskas")

    def __repr__(self):
        return f'<Traffic at {self.location} - Volume: {self.volume}, Avg Speed: {self.average_speed}km/h>'
