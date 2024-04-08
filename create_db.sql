CREATE TABLE "planets" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR,
  "system_id" INTEGER REFERENCES "systems" ("id"),
  "resources_id" INTEGER REFERENCES "resources" ("id")
);

CREATE TABLE "systems" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR,
  "planet_ids" INTEGER[]
);

CREATE TABLE "resources" (
  "id" SERIAL PRIMARY KEY,
  "type" VARCHAR
);

CREATE TABLE "planets_resources" (
  "planet_id" INTEGER REFERENCES "planets" ("id"),
  "resource_id" INTEGER REFERENCES "resources" ("id"),
  PRIMARY KEY ("planet_id", "resource_id")
);

CREATE TABLE "systems_resources" (
  "system_id" INTEGER REFERENCES "systems" ("id"),
  "resource_id" INTEGER REFERENCES "resources" ("id"),
  PRIMARY KEY ("system_id", "resource_id")
);
