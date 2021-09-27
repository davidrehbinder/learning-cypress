#!/usr/bin/env python3

import datetime
import sqlite3
from random import randint

con = sqlite3.connect('database.db')
cur = con.cursor()

def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS posts(id INTEGER NOT
        NULL UNIQUE, username TEXT NOT NULL, headline TEXT NOT NULL,
        content TEXT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS sessions(sid INTEGER NOT
        NULL UNIQUE, username TEXT NOT NULL, expires TEXT NOT NULL)''')
    con.commit()

def generate_sid():
    return ''.join(str(randint(1,9)) for _ in range(10))

def login_user(user, password):
    cur.execute('''SELECT 1 FROM users WHERE username = ?
        AND password = ?''', (user, password))
    status = cur.fetchall()
    if len(status) != 1 or status[0][0] != 1:
        return ['FAILURE', False]
    elif status[0][0] == 1:
        sid = generate_sid()
        expires = str(datetime.datetime.now() + datetime.timedelta(hours=1))
        cur.execute('''INSERT INTO sessions(sid, username, expires) VALUES (?,?,?)''',
            (sid, user, expires))
        con.commit()
        return ['SUCCESS', sid]
    else:
        return ['ERROR', False]

def check_session(sid, user):
    cur.execute('''SELECT * FROM sessions WHERE sid = ? AND username = ? ORDER BY
        expires DESC LIMIT 1''', (sid, user))
    sids = cur.fetchall()
    sid = int(sid)
    if len(sids) == 0:
        return 'FAILURE'
    session = list(sids[0])
    if len(session) != 3:
        return 'FAILURE'
    if (datetime.datetime.now() > datetime.datetime.strptime(session[2], '%Y-%m-%d %H:%M:%S.%f')):
        return 'EXPIRED'
    elif session[0] != sid:
        return 'FAILURE'
    elif session[0] == sid:
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

def delete_sessions(user):
    cur.execute('''SELECT 1 FROM sessions WHERE username = ?''', (user,))
    session = cur.fetchall()
    print(list(session[0]))
    if not (session == []):
        cur.execute('''DELETE FROM sessions WHERE username = ?''', (user,))
        con.commit()
        cur.execute('''VACUUM''')
