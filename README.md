# MockAccidentAPI

MockAccidentAPI is a lightweight Flask-based RESTful API designed to simulate traffic accidents on specific routes. This API enables developers and researchers to generate and utilize mock accident data to improve route choices and traffic safety. The API uses SQLite for storing and managing accident data.

## Features

- **Accident Data Creation:** Users can create fictional accident data including location, description, and time.
- **Data Retrieval:** The API provides endpoints for retrieving and listing accident data.
- **Simple Integration:** The clear and straightforward interface of the API makes it easily integrable with existing projects.

## Technologies

- **Backend:** Python + Flask
- **Database:** SQLite
- **Testing:** unittest (Python's standard library)

## Deployment

### Clone the Repository

git clone [https://github.com/yourusername/MockAccidentAPI.git](https://github.com/sampokuhalampi/MockAccidentAPI.git)](https://github.com/sampokuhalampi/MockAccidentAPI.git)

## Install Dependencies

Use `pip` to install the dependencies from the `requirements.txt` file:

pip install -r requirements.txt

## Initialize the Database 
Run the Flask shell and create the database tables:

flask shell
from app import db
db.create_all()

## Start the Application
Start the Flask application from the command line:

flask run

The application will by default start at http://127.0.0.1:5000/.

