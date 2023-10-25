DROP TABLE IF EXISTS dates_listings;
DROP SEQUENCE IF EXISTS dates_listings_id_sequence;

DROP TABLE IF EXISTS requests;
DROP SEQUENCE IF EXISTS requests_id_sequence;

DROP TABLE IF EXISTS listings;
DROP SEQUENCE IF EXISTS listings_id_sequence;

DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_sequence;

CREATE SEQUENCE IF NOT EXISTS users_id_sequence;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255)
    );

CREATE SEQUENCE IF NOT EXISTS listings_id_sequence;
CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description VARCHAR(255),
    price numeric(10, 2),
    owner_id int,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
    );

CREATE SEQUENCE IF NOT EXISTS requests_id_sequence;
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    date_requested DATE,
    listing_id int,
    requester_id int,
    confirmed boolean,
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE
    );

CREATE SEQUENCE IF NOT EXISTS dates_listings_id_sequence;
CREATE TABLE dates_listings (
    id SERIAL PRIMARY KEY,
    date_available DATE,
    listing_id int,
    requester_id int,
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE
    );

--We are creating three users
INSERT INTO users (email, password) VALUES ('dan@email.com', 'password');
INSERT INTO users (email, password) VALUES ('dave@email.com', 'lastword');
INSERT INTO users (email, password) VALUES ('claire@email.com', 'passstone');
INSERT INTO users (email, password) VALUES ('onuora@email.com', 'passroad');

--We are adding three listings with user one creating listing one, etc
INSERT INTO listings (title, description, price, owner_id) VALUES ('House 1', 'Small house', 100.00, 1);
INSERT INTO listings (title, description, price, owner_id) VALUES ('House 2', 'Medium house', 150.00, 2);
INSERT INTO listings (title, description, price, owner_id) VALUES ('House 3', 'Big house', 200.00, 3);
INSERT INTO listings (title, description, price, owner_id) VALUES ('House 4', 'Massive house', 500.00, 4);

--We are adding three listings with the dates available
INSERT INTO dates_listings (date_available, listing_id, requester_id) VALUES ('2023-10-24', 1, 3);
INSERT INTO dates_listings (date_available, listing_id, requester_id) VALUES ('2023-10-24', 2, 1);
INSERT INTO dates_listings (date_available, listing_id, requester_id) VALUES ('2023-10-24', 3, 2);
INSERT INTO dates_listings (date_available, listing_id, requester_id) VALUES ('2023-10-24', 4, 1);

--We are adding three requests for the listings that are available
INSERT INTO requests (date_requested, listing_id, requester_id, confirmed) VALUES ('2023-10-24', 1, 3, Null);
INSERT INTO requests (date_requested, listing_id, requester_id, confirmed) VALUES ('2023-10-24', 2, 1, Null);
INSERT INTO requests (date_requested, listing_id, requester_id, confirmed) VALUES ('2023-10-24', 3, 2, Null);
INSERT INTO requests (date_requested, listing_id, requester_id, confirmed) VALUES ('2023-10-24', 4, 1, Null);

