import unittest
from app import app, db
from app.models import Accident, Traffic
from datetime import datetime

class TestCase(unittest.TestCase):

    def setUp(self):
        # Define the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Create database tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop the database tables after the tests
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_accidents(self):
        # Test the GET /accidents endpoint
        response = self.app.get('/accidents')
        self.assertEqual(response.status_code, 200)

    def test_post_accident(self):
        # Test the POST /accidents endpoint
        accident = {
            "location": {"latitude": 65.012088, "longitude": 25.469931},
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "accidentType": "Collision",
            "severity": "Moderate",
            "participants": 2,
            "weatherConditions": "Clear"
        }
        response = self.app.post('/accidents', json=accident)
        self.assertEqual(response.status_code, 201)

    def test_get_accident_by_id(self):
        # First add an accident record for testing
        accident = Accident(latitude=65.012088, longitude=25.469931, timestamp=datetime.utcnow(),
                            accident_type="Collision", severity="Moderate", participants=2, weather_conditions="Clear")
        with app.app_context():
            db.session.add(accident)
            db.session.commit()

        # Test the GET /accidents/{id} endpoint
        response = self.app.get(f'/accidents/{accident.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_traffic(self):
        # Test the GET /traffic endpoint
        response = self.app.get('/traffic')
        self.assertEqual(response.status_code, 200)

    def test_post_traffic(self):
        # Test the POST /traffic endpoint
        traffic = {
            "location": {"latitude": 65.012088, "longitude": 25.469931},
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "volume": 100,
            "averageSpeed": 50,
            "congestionLevel": "Low"
        }
        response = self.app.post('/traffic', json=traffic)
        self.assertEqual(response.status_code, 201)

    def test_get_traffic_by_id(self):
        # First add a traffic record for testing
        traffic = Traffic(latitude=65.012088, longitude=25.469931, timestamp=datetime.utcnow(),
                          volume=100, average_speed=50, congestion_level="Low")
        with app.app_context():
            db.session.add(traffic)
            db.session.commit()

        # Test the GET /traffic/{id} endpoint
        response = self.app.get(f'/traffic/{traffic.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
