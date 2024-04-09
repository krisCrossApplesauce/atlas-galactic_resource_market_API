import csv
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="galactic_db",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Read and insert data into resources table
with open('resource_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("INSERT INTO resources (type) VALUES (%s) RETURNING id;", (row['type'],))
        resource_id = cur.fetchone()[0]

# Read and insert data from system_data.csv
with open('system_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("INSERT INTO systems (id, name) VALUES (%s, %s);", (row['id'], row['name']))

# Read and insert data from planet_data.csv
with open('planet_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("INSERT INTO planets (id, name, system_id) VALUES (%s, %s, %s);", (row['id'], row['name'], row['system']))

# Read and insert data from planet_resource_data.csv
resource_ids = set()
with open('planet_resource_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        resource_id = int(row['resource_id'])
        resource_ids.add(resource_id)

# Double checks resources referenced are in the resources table, avoids multiple
for resource_id in resource_ids:
    cur.execute("SELECT id FROM resources WHERE id = %s", (resource_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO resources (id, type) VALUES (%s, 'Resource %s')", (resource_id, resource_id))

conn.commit()

# Read and insert data from planet_resource_data.csv
with open('planet_resource_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        planet_id = int(row['planet_id'])
        resource_id = int(row['resource_id'])
        cur.execute("SELECT * FROM planet_resources WHERE planet_id = %s AND resource_id = %s", (planet_id, resource_id))
        if not cur.fetchone():
            cur.execute("INSERT INTO planet_resources (planet_id, resource_id) VALUES (%s, %s);", (planet_id, resource_id))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()