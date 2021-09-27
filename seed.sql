CREATE TABLE
    IF NOT EXISTS
        users (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
            );
CREATE TABLE
    IF NOT EXISTS
        posts (
            id INTEGER NOT NULL UNIQUE,
            username TEXT NOT NULL,
            headline TEXT NOT NULL,
            content TEXT NOT NULL
            );
CREATE TABLE
    IF NOT EXISTS
        sessions (
            sid INTEGER NOT NULL UNIQUE,
            username TEXT NOT NULL,
            expires TEXT NOT NULL
            );
REPLACE INTO
    users (
        username,
        password
        )
    VALUES (
        "login_test",
        "login"
        );
