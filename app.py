from flask import Flask, jsonify, render_template
import psycopg2

app = Flask(__name__)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="galactic_db",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/planets')
def get_planets():
    cur.execute("SELECT planets.name, systems.name FROM planets, systems WHERE systems.id=planets.system_id;")
    planets = cur.fetchall()
    return jsonify(planets)

@app.route('/systems')
def get_systems():
    cur.execute("SELECT name FROM systems")
    systems = cur.fetchall()
    return jsonify(systems)

@app.route('/resources')
def get_resources():
    cur.execute("SELECT type FROM resources")
    resources = cur.fetchall()
    return jsonify(resources)

@app.route('/planet_resources')
def get_planet_resources():
    cur.execute("SELECT planets.name, resources.type FROM planets, resources WHERE EXISTS (SELECT * FROM planet_resources WHERE planets.id=planet_resources.planet_id AND resources.id=planet_resources.resource_id );")
    planet_resources = cur.fetchall()
    return jsonify(planet_resources)

@app.route('/planets/<resource_type>', methods=['GET'])
def get_planets_by_resource(resource_type):
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN planet_resources ON planets.id = planet_resources.planet_id 
        JOIN resources ON planet_resources.resource_id = resources.id 
        WHERE LOWER(resources.type) = LOWER(%s)
    """, (resource_type,))
    planets = cur.fetchall()
    if not planets:
        return jsonify({'message': 'No planets found with the specified resource'}), 404
    return jsonify(planets)

@app.route('/<system_name>/planets', methods=['GET'])
def get_planets_in_system(system_name):
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN systems ON planets.system_id = systems.id
        WHERE LOWER(systems.name) = LOWER(%s);
    """, (system_name,))
    planets = cur.fetchall()
    if not planets:
        return jsonify({'message': 'No planets found within the specified system'}), 404
    return jsonify(planets)

@app.route('/<system_name>/planets/<resource_type>', methods=['GET'])
def get_planets_in_system_by_resource(system_name, resource_type):
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN systems ON planets.system_id = systems.id
        JOIN planet_resources ON planets.id = planet_resources.planet_id 
        JOIN resources ON planet_resources.resource_id = resources.id 
        WHERE LOWER(systems.name) = LOWER(%s) 
        AND LOWER(resources.type) = LOWER(%s);
    """, (system_name, resource_type,))
    planets = cur.fetchall()
    if not planets:
        return jsonify({'message': 'No planets found with the specified resource within the specified system'}), 404
    return jsonify(planets)

@app.route('/<planet_name>/resources', methods=['GET'])
def get_resources_on_planet(planet_name):
    cur.execute("""
        SELECT resources.type 
        FROM resources 
        JOIN planet_resources ON resources.id = planet_resources.resource_id 
        JOIN planets ON planet_resources.planet_id = planets.id 
        WHERE LOWER(planets.name) = LOWER(%s);
    """, (planet_name,))
    resources = cur.fetchall()
    if not resources:
        return jsonify({'message': 'No resources found on the specified planet'}), 404
    return jsonify(resources)


if __name__ == '__main__':
    app.run(debug=True)
