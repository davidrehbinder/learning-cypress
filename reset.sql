CREATE TABLE
    IF NOT EXISTS
        users (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
            );
DELETE FROM users;