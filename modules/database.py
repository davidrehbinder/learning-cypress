#!/usr/bin/env python3

import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS posts(id INTEGER NOT
        NULL UNIQUE, username TEXT NOT NULL, headline TEXT NOT NULL,
        content TEXT NOT NULL)''')
    con.commit()

def login_user(user, password):
    cur.execute('''SELECT 1 FROM users WHERE username = ?
        AND password = ?''', (user, password))
    status = cur.fetchall()
    if len(status) != 1 or status[0][0] != 1:
        return 'FAILURE'
    elif status[0][0] == 1:
        return 'SUCCESS'
    else:
        return 'ERROR'

def create_user(user, password):
    cur.execute('''SELECT 1 FROM users WHERE username = ?''',
        (user,))
    exists = cur.fetchall()
    if len(exists) != 1 or exists[0][0] != 1:
        try:
            if len(password) < 4:
                return 'TOO_SHORT'
            else:
                cur.execute('''INSERT INTO users(username, password)
                    VALUES (?,?)''', (user, password))
                con.commit()
                return 'SUCCESS'
        except sqlite3.Error as e:
            print('An error occurred:', e.args[0])
            return 'ERROR'
    else:
        return 'USER_EXISTS'

def create_post(user, headline, content):
    cur.execute('''SELECT id FROM posts ORDER BY id DESC LIMIT 1''')
    id = cur.fetchall()
    return_data = []
    if len(id) != 1:
        next_id = 1
    else:
        next_id = id[0][0] + 1
    try:
        print(next_id, user, headline, content)
        cur.execute('''INSERT INTO posts(id, username, headline, content)
            VALUES(?,?,?,?)''', (next_id, user, headline, content))
        con.commit()
        return_data = ['SUCCESS', next_id]
        return return_data
    except sqlite3.Error as e:
        print('An error occurred:', e.args[0])
        return ['ERROR']
