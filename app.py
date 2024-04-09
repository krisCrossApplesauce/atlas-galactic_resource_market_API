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
    cur.execute("SELECT * FROM planet_resources")
    planet_resources = cur.fetchall()
    return jsonify(planet_resources)

if __name__ == '__main__':
    app.run(debug=True)
