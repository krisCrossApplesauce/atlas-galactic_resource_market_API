CREATE TABLE systems (
  id SERIAL PRIMARY KEY,
  name VARCHAR
);

CREATE TABLE planets (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  system_id INT REFERENCES systems(id)
);

CREATE TABLE resources (
  id SERIAL PRIMARY KEY,
  type VARCHAR
);

CREATE TABLE planet_resources (
  planet_id INT REFERENCES planets(id),
  resource_id INT REFERENCES resources(id),
  PRIMARY KEY (planet_id, resource_id)
);

ALTER TABLE planets ADD FOREIGN KEY (system_id) REFERENCES systems(id);
ALTER TABLE planet_resources ADD FOREIGN KEY (planet_id) REFERENCES planets(id);
ALTER TABLE planet_resources ADD FOREIGN KEY (resource_id) REFERENCES resources(id);
