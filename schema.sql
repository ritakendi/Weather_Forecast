DROP TABLE IF EXISTS users;

CREATE TABLE users (
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    email UNIQUE NOT NULL,
    password TEXT NOT NULL
);