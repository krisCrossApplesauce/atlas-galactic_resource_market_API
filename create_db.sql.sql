CREATE TABLE "planets" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "system" integer,
  "resources" varchar
  -- "quantities" varchar
);

CREATE TABLE "systems" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "planets" varchar,
  "resources" varchar
);

CREATE TABLE "resources" (
  "id" integer PRIMARY KEY,
  "type" varchar,
  "systems" varchar,
  "planets" varchar
  -- "quantities" varchar
);

CREATE TABLE "planets_resources" (
  "planets_resources" varchar,
  "resources_planets" varchar,
  PRIMARY KEY ("planets_resources", "resources_planets")
);

ALTER TABLE "planets_resources" ADD FOREIGN KEY ("planets_resources") REFERENCES "planets" ("resources");

ALTER TABLE "planets_resources" ADD FOREIGN KEY ("resources_planets") REFERENCES "resources" ("planets");


ALTER TABLE "planets" ADD FOREIGN KEY ("system") REFERENCES "systems" ("planets");

CREATE TABLE "systems_resources" (
  "systems_resources" varchar,
  "resources_systems" varchar,
  PRIMARY KEY ("systems_resources", "resources_systems")
);

ALTER TABLE "systems_resources" ADD FOREIGN KEY ("systems_resources") REFERENCES "systems" ("resources");

ALTER TABLE "systems_resources" ADD FOREIGN KEY ("resources_systems") REFERENCES "resources" ("systems");

