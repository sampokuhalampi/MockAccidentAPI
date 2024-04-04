from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Define the database path
database_path = 'ASD-database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

# Initialize blueprints for routing
from app.routes.accidents import accidents_bp
from app.routes.traffic import traffic_bp

app.register_blueprint(accidents_bp, url_prefix='/accidents')
app.register_blueprint(traffic_bp, url_prefix='/traffic')

def recreate_database():
    """Remove the existing database file and recreate the database."""
    if os.path.exists(database_path):
        os.remove(database_path)
        print("Old database file removed.")
    with app.app_context():
        db.create_all()
        print("Database recreated.")

# Call the function to recreate the database
recreate_database()
