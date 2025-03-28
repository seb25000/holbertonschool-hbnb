-- SQL script for creating the HBnB database schema and inserting initial data

-- Drop tables if they exist (for development/testing purposes)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS place;
DROP TABLE IF EXISTS amenity;
DROP TABLE IF EXISTS user;

-- Create User table
CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create Place table
CREATE TABLE place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES user(id)
);

-- Create Review table
CREATE TABLE review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT,
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (place_id) REFERENCES place(id),
    CONSTRAINT unique_user_place UNIQUE (user_id, place_id),
    CHECK (rating BETWEEN 1 AND 5)
);

-- Create Amenity table
CREATE TABLE amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

-- Create Place_Amenity table (Many-to-Many relationship)
CREATE TABLE place_amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES place(id),
    FOREIGN KEY (amenity_id) REFERENCES amenity(id),
    PRIMARY KEY (place_id, amenity_id)
);

-- Insert initial data

-- Insert Administrator User
INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$JzS9J0.u4g5XU2.D/Jj/v.y8p.q.b.r0F6v.v.W3b0h.s.q8iS.',  -- bcrypt hash of "admin1234"
    TRUE
);

-- Insert Initial Amenities (Generate UUIDs for each)
--  Use online generator or python script to create these UUIDs

-- Example UUIDs (replace with your generated values)
-- WiFi: a3e1322a-6a82-4dbb-8b45-5a9d06f936b0
-- Swimming Pool: 79705918-3488-459b-a049-1f766c463640
-- Air Conditioning: e583177f-2382-48f5-b944-a28d400d6039

INSERT INTO amenity (id, name)
VALUES (
    'a3e1322a-6a82-4dbb-8b45-5a9d06f936b0',
    'WiFi'
);

INSERT INTO amenity (id, name)
VALUES (
    '79705918-3488-459b-a049-1f766c463640',
    'Swimming Pool'
);

INSERT INTO amenity (id, name)
VALUES (
    'e583177f-2382-48f5-b944-a28d400d6039',
    'Air Conditioning'
);


-- Test CRUD Operations
-- SELECT statements
SELECT * FROM user;
SELECT * FROM place;
SELECT * FROM review;
SELECT * FROM amenity;
SELECT * FROM place_amenity;

-- INSERT statements (example)
-- Requires you to generate UUIDs for new entries

--Insert a new user
--INSERT INTO user (id, first_name, last_name, email, password, is_admin) VALUES ('7580880e-f5d6-4e14-9dd5-8d16192d9047', 'Test', 'User', 'test@example.com', '$2b$12$JzS9J0.u4g5XU2.D/Jj/v.y8p.q.b.r0F6v.v.W3b0h.s.q8iS.', FALSE);

-- UPDATE statement (example)
UPDATE user SET first_name = 'Administrator' WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- DELETE statement (example - use with caution!)
-- Be VERY careful with deleting data
--DELETE FROM amenity WHERE name = 'Swimming Pool';
