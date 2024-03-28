import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # It's a really bad practice to store the API key in the code 
    # -> This would be fixed if it were used for something other than the test.
    API_KEY = 'ASDAPIkey'
