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

# default page
@app.route('/', strict_slashes=False)
def landing_page():
    return render_template('landing.html')

# lists planets and their system
@app.route('/planets', strict_slashes=False)
def get_planets():
    cur.execute("SELECT planets.name, systems.name FROM planets, systems WHERE systems.id=planets.system_id;")
    planets = cur.fetchall()
    return jsonify(planets)

# lists systems
@app.route('/systems', strict_slashes=False)
def get_systems():
    cur.execute("SELECT name FROM systems")
    systems = cur.fetchall()
    return jsonify(systems)

# lists resources
@app.route('/resources', strict_slashes=False)
def get_resources():
    cur.execute("SELECT type FROM resources")
    resources = cur.fetchall()
    return jsonify(resources)

# lists info about any specified system, resource, or planet
@app.route('/<anything>', methods=['GET'], strict_slashes=False)
def get_info_of_anything_specified(anything):
    if anything == "guk":
        anything = "gük"
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN systems ON planets.system_id = systems.id
        WHERE LOWER(systems.name) = LOWER(%s);
    """, (anything,))
    system_info = cur.fetchall()
    if system_info:
        return jsonify(system_info)
    cur.execute("""
        SELECT planets.name, systems.name 
        FROM planets
        JOIN systems ON planets.system_id = systems.id
        JOIN planet_resources ON planets.id = planet_resources.planet_id 
        JOIN resources ON planet_resources.resource_id = resources.id 
        WHERE LOWER(resources.type) = LOWER(%s);
    """, (anything,))
    resource_info = cur.fetchall()
    if resource_info:
        return jsonify(resource_info)
    cur.execute("""
        SELECT systems.name 
        FROM systems 
        JOIN planets ON planets.system_id = systems.id
        WHERE LOWER(planets.name) = LOWER(%s);
    """, (anything,))
    planet_system = cur.fetchall()
    cur.execute("""
        SELECT resources.type 
        FROM resources 
        JOIN planet_resources ON resources.id = planet_resources.resource_id 
        JOIN planets ON planet_resources.planet_id = planets.id 
        WHERE LOWER(planets.name) = LOWER(%s);
    """, (anything,))
    planet_resources = cur.fetchall()
    if planet_system and planet_resources:
        return jsonify([planet_system, planet_resources])
    return jsonify({'message': 'The specified system, planet, or resource is not in our database :/ Sorry'}), 404

# lists planets and resources
@app.route('/planet_resources', strict_slashes=False)
def get_planet_resources():
    cur.execute("SELECT planets.name, resources.type FROM planets, resources WHERE EXISTS (SELECT * FROM planet_resources WHERE planets.id=planet_resources.planet_id AND resources.id=planet_resources.resource_id );")
    planet_resources = cur.fetchall()
    return jsonify(planet_resources)

# lists all planets that have a specified resource
@app.route('/planets/<resource_type>', methods=['GET'], strict_slashes=False)
def get_planets_by_resource(resource_type):
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN planet_resources ON planets.id = planet_resources.planet_id 
        JOIN resources ON planet_resources.resource_id = resources.id 
        WHERE LOWER(resources.type) = LOWER(%s);
    """, (resource_type,))
    planets = cur.fetchall()
    if not planets:
        return jsonify({'message': 'No planets found with the specified resource'}), 404
    return jsonify(planets)

# lists all planets within a specified system
@app.route('/<system_name>/planets', methods=['GET'], strict_slashes=False)
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

# returns the system that the specified planet is in
@app.route('/<planet_name>/system', methods=['GET'], strict_slashes=False)
def get_system_of_planet(planet_name):
    cur.execute("""
        SELECT systems.name 
        FROM systems 
        JOIN planets ON planets.system_id = systems.id
        WHERE LOWER(planets.name) = LOWER(%s);
    """, (planet_name,))
    system = cur.fetchall()
    if not system:
        return jsonify({'message': 'Planet not found/system for planet not found'}), 404
    return jsonify(system)

# lists the planets within the specified system that contain the specified resource
@app.route('/<system_name>/planets/<resource_type>', methods=['GET'], strict_slashes=False)
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

# lists the resources of a specified planet
@app.route('/<planet_name>/resources', methods=['GET'], strict_slashes=False)
def get_resources_on_planet(planet_name):
    if planet_name == "guk":
        planet_name = "gük"
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

# lists the resources of a specified planet within a specified system
@app.route('/<system_name>/<planet_name>/resources', methods=['GET'], strict_slashes=False)
def get_resources_on_planet_in_system(system_name, planet_name):
    if planet_name == "guk":
        planet_name = "gük"
    cur.execute("""
        SELECT resources.type 
        FROM resources 
        JOIN planet_resources ON resources.id = planet_resources.resource_id 
        JOIN planets ON planet_resources.planet_id = planets.id 
        JOIN systems ON planets.system_id = systems.id 
        WHERE LOWER(systems.name) = LOWER(%s)
        AND LOWER(planets.name) = LOWER(%s);
    """, (system_name, planet_name,))
    resources = cur.fetchall()
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN systems ON planets.system_id = systems.id
        WHERE LOWER(systems.name) = LOWER(%s) 
        AND LOWER(planets.name) = LOWER(%s);
    """, (system_name, planet_name,))
    planet = cur.fetchall()
    if not resources:
        if not planet:
            return jsonify({'message': 'The specified planet could not be found within the specified system'}), 404
        return jsonify({'message': 'No resources found on the specified planet within the specified system'}), 404
    return jsonify(resources)


# lists either:
# the planets within the specified system that contain the specified resource
# or the resources of a specified planet within a specified system
@app.route('/<system_name>/<planet_or_resource>', methods=['GET'], strict_slashes=False)
def get_planets_or_resource_in_system(system_name, planet_or_resource):
    if planet_or_resource == "guk":
        planet_or_resource = "gük"
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN systems ON planets.system_id = systems.id
        JOIN planet_resources ON planets.id = planet_resources.planet_id 
        JOIN resources ON planet_resources.resource_id = resources.id 
        WHERE LOWER(systems.name) = LOWER(%s) 
        AND LOWER(resources.type) = LOWER(%s);
    """, (system_name, planet_or_resource,))
    planets = cur.fetchall()
    if planets:
        return jsonify(planets)
    cur.execute("""
        SELECT resources.type 
        FROM resources 
        JOIN planet_resources ON resources.id = planet_resources.resource_id 
        JOIN planets ON planet_resources.planet_id = planets.id 
        JOIN systems ON planets.system_id = systems.id 
        WHERE LOWER(systems.name) = LOWER(%s)
        AND LOWER(planets.name) = LOWER(%s);
    """, (system_name, planet_or_resource,))
    resources = cur.fetchall()
    cur.execute("""
        SELECT planets.name 
        FROM planets 
        JOIN systems ON planets.system_id = systems.id
        WHERE LOWER(systems.name) = LOWER(%s) 
        AND LOWER(planets.name) = LOWER(%s);
    """, (system_name, planet_or_resource,))
    planet = cur.fetchall()
    if resources and planet:
        return jsonify(resources)
    if not resources:
        if not planet:
            return jsonify({'message': 'The specified planet or resource could not be found within the specified system'}), 404
        return jsonify({'message': 'No resources found on the specified planet within the specified system'}), 404


if __name__ == '__main__':
    app.run(debug=True)
