CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	firstName VARCHAR NOT NULL,
	lastName VARCHAR NOT NULL, 
	username VARCHAR NOT NULL,
	password VARCHAR NOT NULL

);

INSERT INTO users (id, firstName, lastName, username, password) VALUES (Mattie, Krop, mattiek, testing)