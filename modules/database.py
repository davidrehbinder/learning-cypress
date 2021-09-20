#!/usr/bin/env python3

import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    con.commit()

def check_user(user, password):
    cur.execute('''SELECT 1 FROM users WHERE username = ?
        AND password = ?''', (user, password))
    status = cur.fetchall()
    try:
        if len(status) != 1:
            return 'FAILURE'
        elif status[0][0] != 1:
            return 'FAILURE'
        elif status[0][0] == 1:
            return 'SUCCESS'
        else:
            return 'FAILURE'
    except:
        return 'FAILURE'

def create_user(user, password):
    try:
        cur.execute('''INSERT INTO users(username, password)
            VALUES (?,?)''', (user, password))
        con.commit()
        return 'SUCCESS'
    except sqlite3.Error as e:
        print('An error occurred:', e.args[0])
        return 'FAILURE'