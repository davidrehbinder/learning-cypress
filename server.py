#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sqlite3
from modules import database

from socketserver import ThreadingMixIn
from http.server import HTTPServer

PORT = 8080

def tables():
    con = sqlite3.connect('database.db', check_same_thread=False)
    cur = con.cursor()
    database.create_tables(con, cur)

tables()
serve_from = os.getcwd()

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        path = serve_from + self.path
        print(self.path)

        self.user = False

        cookies = self.parse_cookies(self.headers['Cookie'])
        if cookies != None:
            if 'username' and 'sid' in cookies:
                username = cookies['username']
                cookie_sid = cookies['sid']
                con = sqlite3.connect('database.db', check_same_thread=False)
                cur = con.cursor()

                session = database.check_session(cur, cookie_sid, username)
                if session == 'SUCCESS':
                    self.user = username
                else:
                    self.user = False
            else:
                self.user = False
        else:
            self.user = False

        if not os.path.abspath(path).startswith(serve_from):
            self.send_response(403)
            if self.user == False:
                self.clear_cookies()
            self.end_headers()
            self.wfile.write(b'Private!')
        elif self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    data = f.read()
                self.send_response(200)
                if self.user == False:
                    self.clear_cookies()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_response(500)
                if self.user == False:
                    self.clear_cookies()
                self.end_headers()
                self.wfile.write(b'Error')
        elif self.path == '/loggedin.html':
            try:
                if self.user != False:
                    with open('loggedin.html', 'rb') as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(data)
                else:
                    self.send_response(403)
                    self.clear_cookies()
                    self.end_headers()
                    self.wfile.write(b'Forbidden')
            except Exception:
                self.send_response(500)
                if self.user == False:
                    self.clear_cookies()
                self.end_headers()
                self.wfile.write(b'Error')
        elif self.path == '/post.json':
            try:
                self.get_posts()
            except Exception:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Error')
        elif os.path.isdir(path):
            try:
                self.send_response(200)
                if self.user == False:
                    self.clear_cookies()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(str(os.listdir(path)).encode())
            except Exception:
                self.send_response(500)
                if self.user == False:
                    self.clear_cookies()
                self.end_headers()
                self.wfile.write(b'error')
        else:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                if self.user == False:
                    self.clear_cookies()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_response(500)
                if self.user == False:
                    self.clear_cookies()
                self.end_headers()
                self.wfile.write(b'error')

    def do_POST(self):

        cookies = self.parse_cookies(self.headers['Cookie'])

        if cookies != None:
            if 'username' and 'sid' in cookies:
                username = cookies['username']
                cookie_sid = cookies['sid']
                con = sqlite3.connect('database.db', check_same_thread=False)
                cur = con.cursor()

                session = database.check_session(cur, cookie_sid, username)
                if session == 'SUCCESS':
                    self.user = username
                else:
                    self.user = False
            else:
                self.user = False
        else:
            self.user = False
        print(self.path)

        if (self.path == '/login.json'):
            self.login()

        if (self.path == '/logout.json'):
            self.logout()

        if (self.path == '/create_user.json'):
            self.create_user()

        if (self.path == '/post.json'):
            self.create_post()

    def login(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(str(self.rfile.read(content_len), encoding='utf-8'))
        print('Request payload: ' + json.dumps(post_body))
        username = post_body['username']
        password = post_body['password']
        con = sqlite3.connect('database.db', check_same_thread=False)
        cur = con.cursor()

        login_status = database.login_user(con, cur, username, password)

        if login_status[0] == 'SUCCESS':
            sid = login_status[1]
            self.send_response(200)
            self.cookies = ['sid={}'.format(sid), 'username='+username]
            for cookie in range(0, len(self.cookies)):
                self.send_header('Set-Cookie', self.cookies[cookie] + ';max-age=3600;path=/')
            return_object = {'login': 'success'}
            print('login successful for ' + username)
        elif login_status[0] == 'FAILURE':
            return_object = {'login': 'failure'}
            self.send_response(200)
            print('login failed for ' + username)
        else:
            return_object = {'login': 'error'}
            self.send_response(500)
            print('login error for ' + username)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(str(json.dumps(return_object)), encoding='utf-8'))

    def logout(self):
        self.send_response(200)
        if self.user != False:
            con = sqlite3.connect('database.db', check_same_thread=False)
            cur = con.cursor()

            database.delete_sessions(con, cur, self.user)
        self.clear_cookies()
        self.end_headers()
        if not self.user:
            self.wfile.write(bytes(str(json.dumps({'logout': 'not_logged_in'})), encoding='utf-8'))
        else:
            self.wfile.write(bytes(str(json.dumps({'logout': 'success'})), encoding='utf-8'))

    def clear_cookies(self):
        self.cookies = ['sid=', 'username=']
        for cookie in range(0,len(self.cookies)):
            self.send_header('Set-Cookie', self.cookies[cookie] + ';max-age=0;path=/')

    def create_user(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(str(self.rfile.read(content_len), encoding='utf-8'))
        print('Request payload: ' + json.dumps(post_body))
        username = post_body['username']
        password = post_body['password']

        con = sqlite3.connect('database.db', check_same_thread=False)
        cur = con.cursor()
        user_creation_status = database.create_user(con, cur, username, password)

        if user_creation_status == 'SUCCESS':
            return_object = {'user_creation': 'success', 'username': username}
            self.send_response(200)
            print('user creation successful for ' + username)
        elif user_creation_status == 'USER_EXISTS':
            return_object = {'user_creation': 'user_exists', 'username': username}
            self.send_response(200)
            print('user already exists error for ' + username)
        elif user_creation_status == 'TOO_SHORT':
            return_object = {'user_creation': 'too_short'}
            self.send_response(200)
            print('password too short for ' + username)
        else:
            return_object = {'user_creation': 'error'}
            self.send_response(500)
            print('user creation error for ' + username)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(str(json.dumps(return_object)), encoding='utf-8'))

    def create_post(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(str(self.rfile.read(content_len), encoding='utf-8'))
        print('Request payload: ' + json.dumps(post_body))
        if 'username' not in post_body:
            return_object = {'post_creation': 'failure'}
            self.send_response(403)
            print('unauthorised access attempt')
        else:
            username = post_body['username']
            if self.user != username:
                return_object = {'post_creation': 'failure'}
                self.send_response(403)
                print('unauthorised access attempt by ' + username)
            else:
                headline = post_body ['headline']
                content = post_body['content']

                con = sqlite3.connect('database.db', check_same_thread=False)
                cur = con.cursor()

                post_creation_status = database.create_post(con, cur, username, headline, content)
                if post_creation_status[0] == 'SUCCESS':
                    post_id = post_creation_status[1]
                    return_object = {'post_creation': 'success', 'post_id': post_id}
                    self.send_response(200)
                    print('post creation successful for ' + username + ', id ' + str(post_id))
                else:
                    return_object = {'post_creation': 'error'}
                    self.send_response(500)
                    print('post creation error for ' + username)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(str(json.dumps(return_object)), encoding='utf-8'))

    def get_posts(self):
        con = sqlite3.connect('database.db', check_same_thread=False)
        cur = con.cursor()
        post_list = database.get_posts(cur)
        if post_list['status'] == 'NO_POSTS':
            return_object = {'status': 'no_posts'}
        elif post_list['status'] == 'SUCCESS':
            return_object = {'status': 'success', 'posts': post_list['posts']}
        elif post_list['status'] == 'ERROR':
            return_object = {'status': 'error'}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(str(json.dumps(return_object)), encoding='utf-8'))

    def parse_cookies(self, cookie_list):
        if cookie_list:
            list_cookie = {}
            c = cookie_list.split(';')
            for cookie in range(0,len(c)):
                list_cookie[c[cookie].split('=')[0].lstrip()] = c[cookie].split('=')[1]
            return list_cookie

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

print('Server started on ', PORT)

def run():
    server = ThreadingSimpleServer(('0.0.0.0', PORT), MyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    run()
