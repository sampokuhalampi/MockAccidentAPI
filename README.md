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

git clone https://github.com/sampokuhalampi/MockAccidentAPI.git

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

## Running Tests

This project includes a set of unit tests to ensure the functionality works as expected. The tests are located in the `tests` directory.

### Prerequisites

Before running the tests, make sure you have all the necessary dependencies installed. You can install them using the following command:

pip install -r requirements.txt

## Running all Tests

To run all tests, navigate to the tests directory of the project and use the following command:

python -m unittest discover tests

This command will discover all test files in the tests directory and execute them.

## Running Specific Tests

If you wish to run a specific test, you can do so by specifying the path to the test file and the test case name. For example:

python -m unittest tests.test_app.TestCase.test_get_accidents

This command will only run the test_get_accidents test within the TestCase class in the test_app.py file located in the tests directory.

## Test Output

The output will show you which tests passed successfully and which failed, including any error messages or stack traces for the failed tests.

Please make sure to review the test results and fix any issues before pushing changes to the repository.
