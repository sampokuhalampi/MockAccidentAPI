import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ASD-database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Keep your API_KEY here (ensure it matches the one used in API calls)
    API_KEY = os.environ['API_KEY']
