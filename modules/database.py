#!/usr/bin/env python3

import datetime
import sqlite3
from random import randint

# con = sqlite3.connect('database.db', check_same_thread=False)
# cur = con.cursor()

def create_tables(con, cur):
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

def login_user(con, cur, user, password):
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

def check_session(cur, sid, user):
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

def create_user(con, cur, user, password):
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

def create_post(con, cur, user, headline, content):
    cur.execute('''SELECT id FROM posts ORDER BY id DESC LIMIT 1''')
    id = cur.fetchall()
    return_data = []
    if len(id) != 1:
        next_id = 1
    else:
        next_id = id[0][0] + 1
    try:
        cur.execute('''INSERT INTO posts(id, username, headline, content)
            VALUES(?,?,?,?)''', (next_id, user, headline, content))
        con.commit()
        return_data = ['SUCCESS', next_id]
        return return_data
    except sqlite3.Error as e:
        print('An error occurred:', e.args[0])
        return ['ERROR']

def get_posts(cur):
    cur.execute('''SELECT * from posts''')
    posts = cur.fetchall()
    if posts == []:
        return_data = {'status': 'NO_POSTS'}
    elif len(posts) > 0:
        post_list = []
        for i in range(0, len(posts)):
            post_entry = {'id': posts[i][0], 'username': posts[i][1], 'headline': posts[i][2], 'content': posts[i][3]}
            post_list.append(post_entry)
        return_data = {'status': 'SUCCESS', 'posts': post_list}
    else:
        return_data = {'status': 'ERROR'}
    print(return_data['status'])
    return return_data

def delete_sessions(con, cur, user):
    cur.execute('''SELECT 1 FROM sessions WHERE username = ?''', (user,))
    session = cur.fetchall()
    if not (session == []):
        cur.execute('''DELETE FROM sessions WHERE username = ?''', (user,))
        con.commit()
        cur.execute('''VACUUM''')
