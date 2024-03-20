import unittest
from app import app, db
from app.models import Accident, Traffic
from datetime import datetime

class TestCase(unittest.TestCase):

    def setUp(self):
        print("Setting up test environment...")
        # Define the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.headers = {'API-Key': 'ASDAPIkey'}  # Korvaa tämä omalla API-avaimellasi

        # Create database tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        print("Tearing down test environment...")
        # Drop the database tables after the tests
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_accidents(self):
        print("Testing GET /accidents endpoint...")
        # Test the GET /accidents endpoint with API key
        response = self.app.get('/accidents', headers=self.headers)
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_post_accident(self):
        print("Testing POST /accidents endpoint...")
        # Test the POST /accidents endpoint with API key
        accident = {
            "latitude": 65.012088, 
            "longitude": 25.469931,
            "timestamp": datetime.utcnow().isoformat(),
            "accident_type": "Collision",
            "severity": "Moderate",
            "participants": 2,
            "weather_conditions": "Clear"
        }
        response = self.app.post('/accidents', json=accident, headers=self.headers)
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 201)

    def test_get_accident_by_id(self):
        print("Testing GET /accidents/{id} endpoint...")
        # First add an accident record for testing with API key
        accident = Accident(latitude=65.012088, longitude=25.469931, timestamp=datetime.utcnow(),
                            accident_type="Collision", severity="Moderate", participants=2, weather_conditions="Clear")
        with app.app_context():
            db.session.add(accident)
            db.session.commit()
            accident_id = accident.id  # Fetch the accident ID

        # Test the GET /accidents/{id} endpoint with API key
        response = self.app.get(f'/accidents/{accident_id}', headers=self.headers)
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_get_traffic(self):
        print("Testing GET /traffic endpoint...")
        # Test the GET /traffic endpoint with API key
        response = self.app.get('/traffic', headers=self.headers)
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_post_traffic(self):
        print("Testing POST /traffic endpoint...")
        # Test the POST /traffic endpoint with API key
        traffic = {
            "latitude": 65.012088, 
            "longitude": 25.469931,
            "timestamp": datetime.utcnow().isoformat(),
            "volume": 100,
            "averageSpeed": 50,
            "congestionLevel": "Low"
        }
        response = self.app.post('/traffic', json=traffic, headers=self.headers)
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 201)

    def test_get_traffic_by_id(self):
        print("Testing GET /traffic/{id} endpoint...")
        # First add a traffic record for testing with API key
        traffic = Traffic(latitude=65.012088, longitude=25.469931, timestamp=datetime.utcnow(),
                          volume=100, average_speed=50, congestion_level="Low")
        with app.app_context():
            db.session.add(traffic)
            db.session.commit()
            traffic_id = traffic.id  # Fetch the traffic ID

        # Test the GET /traffic/{id} endpoint with API key
        response = self.app.get(f'/traffic/{traffic_id}', headers=self.headers)
        print("Response status code:", response.status_code)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
