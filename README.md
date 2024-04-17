# Atlas Galactic Resource Market API

The Atlas Galactic Resource Market project is designed to help users manage the resources across different planetary systems in the galaxy. It features a backend API for resource management and a frontend interface for users to view and explore available resources in the galaxy.

## Technologies Used

- **Python 3**: Programming language used for the API logic
- **Flask**: Lightweight web framework for building the API
- **PostgreSQL**: Database management system for storing data
- **psycopg2**: A PostgreSQL adapter for Python used to interact with the PostgreSQL database from the Flask application.
- **Flask-RESTful**: An extension for Flask that adds support for quickly building REST APIs.
- **unittest**: The built-in Python unit testing framework used to test the API endpoints.
- **Flask-Testing**: An extension for Flask that provides utilities for testing Flask applications.

## API Diagram
![image](https://github.com/krisCrossApplesauce/atlas-galactic_resource_market_API/assets/115739693/23dd8b7c-a49f-4b38-b852-78dc8bdec938)

## Installation

1. Clone repository:

   ```bash
   git clone https://github.com/krisCrossApplesauce/atlas-galactic_resource_market_API

2. Install Dependencies:

   ```bash
    pip install -r requirements.txt

3. Set up PostgreSQL database and confirgure connection in `app.py`.

4. Run app.py in root directory:

   ```bash
   flask run

5. Access the API at `http://localhost:5000/`

## API Endpoints

- `GET /`: Landing page.
- `GET /planets`: List all planets and their systems.
- `GET /systems`: List all systems.
- `GET /resources`: List all resources.
- `GET /<anything>`: Get info about a specified system, resource, or planet.
- `GET /planet_resources`: List all planets and their resources.
- `GET /planets/<resource_type>`: List all planets with a specified resource.
- `GET /<system_name>/planets`: List all planets within a specified system.
- `GET /<planet_name>/system`: Get the system that a specified planet is in.
- `GET /<system_name>/planets/<resource_type>`: List all planets in a system with a specified resource.
- `GET /<planet_name>/resources`: List all resources on a specified planet.
- `GET /<system_name>/<planet_name>/resources`: List all resources on a planet within a specified system.
- `GET /<system_name>/<planet_or_resource>`: List planets or resources within a specified system.

## Authors

- **Cason Bobo** - [casonbobo](https://github.com/casonbobo)
- **Caramon Hofstetter** - [CaramonH](https://github.com/CaramonH)
- **Karis Richardson** - [krisCrossApplesauce](https://github.com/krisCrossApplesauce)
