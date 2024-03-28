import unittest
from app import app, db
from app.models import Accident, Traffic, AccidentCoordinates, TrafficCoordinates
from datetime import datetime

class TestCase(unittest.TestCase):

    def setUp(self):
        print("Setting up test environment...")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.headers = {'API-Key': 'ASDAPIkey'}

        with app.app_context():
            db.create_all()

    def tearDown(self):
        print("Tearing down test environment...")
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_post_accident_with_geometry(self):
        print("Testing POST /accidents endpoint with geometry...")
        accident_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "accident_type": "Collision",
            "severity": "Minor",
            "participants": 2,
            "weather_conditions": "Clear",
            "geometry": [
                [{"latitude": 60.192059, "longitude": 24.945831},
                 {"latitude": 60.193000, "longitude": 24.946000},
                 {"latitude": 60.194000, "longitude": 24.947000}]
            ]
        }
        response = self.app.post('/accidents', json=accident_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_post_accident_without_geometry(self):
        print("Testing POST /accidents endpoint without geometry...")
        accident_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "accident_type": "Collision",
            "severity": "Minor",
            "participants": 2,
            "weather_conditions": "Clear",
            "latitude": 60.192059,
            "longitude": 24.945831
        }
        response = self.app.post('/accidents', json=accident_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_post_traffic_with_geometry(self):
        print("Testing POST /traffic endpoint with geometry...")
        traffic_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "volume": 100,
            "averageSpeed": 60,
            "congestionLevel": "Moderate",
            "geometry": [
                [{"latitude": 60.192059, "longitude": 24.945831},
                 {"latitude": 60.193000, "longitude": 24.946000},
                 {"latitude": 60.194000, "longitude": 24.947000}]
            ]
        }
        response = self.app.post('/traffic', json=traffic_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_post_traffic_without_geometry(self):
        print("Testing POST /traffic endpoint without geometry...")
        traffic_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "volume": 100,
            "averageSpeed": 60,
            "congestionLevel": "Moderate",
            "latitude": 60.192059,
            "longitude": 24.945831
        }
        response = self.app.post('/traffic', json=traffic_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_get_accident_by_id_with_geometry(self):
        print("Testing GET /accidents/{id} endpoint with geometry...")
        accident = Accident(timestamp=datetime.utcnow(), accident_type="Collision", severity="Minor", participants=2, weather_conditions="Clear")
        with app.app_context():
            db.session.add(accident)
            db.session.flush()
            for lat, lon in [(60.192059, 24.945831), (60.193000, 24.946000), (60.194000, 24.947000)]:
                acc_coord = AccidentCoordinates(accident_id=accident.id, latitude=lat, longitude=lon)
                db.session.add(acc_coord)
            db.session.commit()
            accident_id = accident.id

        response = self.app.get(f'/accidents/{accident_id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_traffic_by_id_with_geometry(self):
        print("Testing GET /traffic/{id} endpoint with geometry...")
        traffic = Traffic(timestamp=datetime.utcnow(), volume=100, average_speed=60, congestion_level="Moderate")
        with app.app_context():
            db.session.add(traffic)
            db.session.flush()
            for lat, lon in [(60.192059, 24.945831), (60.193000, 24.946000), (60.194000, 24.947000)]:
                traffic_coord = TrafficCoordinates(traffic_id=traffic.id, latitude=lat, longitude=lon)
                db.session.add(traffic_coord)
            db.session.commit()
            traffic_id = traffic.id

        response = self.app.get(f'/traffic/{traffic_id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()
