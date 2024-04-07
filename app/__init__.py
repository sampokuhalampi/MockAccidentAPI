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

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import models and routes
from app import models
from app.routes import accidents, traffic

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