CREATE DATABASE te1;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INTEGER);

INSERT INTO users (name, age) VALUES
    ('Brian Hugh Warner', 56),
    ('Noah Sebastian', 30), 
    ('Farrukh Bulsara', 58),
    ('Sharon den Adel', 51),
    ('Mike Shinoda', 48),
    ('Paul McCartney', 83),
    ('Eddie Berg', 33),
    ('Harald Barrett', 32),
    ('Anna Murphy', 36),
    ('Chester Charles Bennington', 41),
    ('James Newell Osterberg', 78); 
