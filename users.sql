CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	firstName VARCHAR NOT NULL,
	lastName VARCHAR NOT NULL, 
	username VARCHAR NOT NULL,
	password VARCHAR NOT NULL

);

CREATE TABLE reviews (
	id SERIAL PRIMARY KEY,
	book_id INT NOT NULL,
	user_id INT NOT NULL,
	rating INT NOT NULL,
	review VARCHAR, 
)
INSERT INTO users (id, firstName, lastName, username, password) VALUES (Mattie, Krop, mattiek, testing)