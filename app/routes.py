from app import app, db
from app.models import Accident

@app.route('/')
def index():
    # Esimerkkitoiminto, joka listaa kaikki onnettomuudet
    accidents = Accident.query.all()
    return str(accidents)
