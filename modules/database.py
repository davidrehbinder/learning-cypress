#!/usr/bin/env python3

import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    con.commit()

def login_user(user, password):
    cur.execute('''SELECT 1 FROM users WHERE username = ?
        AND password = ?''', (user, password))
    status = cur.fetchall()
    print(status)
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
            cur.execute('''INSERT INTO users(username, password)
                VALUES (?,?)''', (user, password))
            con.commit()
            return 'SUCCESS'
        except sqlite3.Error as e:
            print('An error occurred:', e.args[0])
            return 'ERROR'
    else:
        return 'FAILURE'
