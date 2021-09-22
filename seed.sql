CREATE TABLE
    IF NOT EXISTS
        users(username
            TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
            );
REPLACE INTO
    users(username, password)
    VALUES("login_test", "login");
