CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    lastName VARCHAR(100),
    firstName VARCHAR(100),
    email VARCHAR(320),
    activities TEXT
);

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    profile_id SERIAL,
    message TEXT,
    dateTime TIMESTAMP,
    FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);
