from app import db

class Accident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Accident {self.location} - {self.description}>'
