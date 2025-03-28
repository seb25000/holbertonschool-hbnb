INSERT INTO Users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2y$10$4OcyuUIeMRjh2cjF3ullvOQrrCUqvBVhaOOS81xkj6htGPwiM7qeW',
    TRUE
);

INSERT INTO Amenity (id, name) VALUES 
    (UUID(), 'WiFi'),
    (UUID(), 'Swimming Pool'),
    (UUID(), 'Air Conditioning');
