from app import app, db
from app.models import Accident 

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Accident': Accident}

if __name__ == '__main__':
    app.run(debug=True)
