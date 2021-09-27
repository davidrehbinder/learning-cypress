#!/usr/bin/env python3

from http import server
import json
import os
from random import randint
import socketserver
from modules import database

PORT = 8080

sessions = {}

database.create_tables()

serve_from = os.getcwd()

class MyHandler(server.BaseHTTPRequestHandler):

    def parse_cookies(self, cookie_list):
        if cookie_list:
            list_cookie = {}
            c = cookie_list.split(';')
            for cookie in range(0,len(c)):
                list_cookie[c[cookie].split('=')[0].lstrip()] = c[cookie].split('=')[1]
            return list_cookie

    def do_GET(self):

        path = serve_from + self.path
        print(self.path)

        clear = True

        cookies = self.parse_cookies(self.headers['Cookie'])
        if sessions != {}:
            if cookies != None:
                if 'username' and 'sid' in cookies:
                    username = cookies['username']
                    if (cookies['sid'] == sessions[username]['sid']):
                        self.user = sessions[username]
                        clear = False
                    else:
                        del sessions[username]
                        self.user = False
                        clear = True
                else:
                    self.user = False
                    clear = True
            else:
                self.user = False
                clear = True
        else:
            self.user = False
            clear = True


        if not os.path.abspath(path).startswith(serve_from):
            self.send_response(403)
            if clear == True:
                self.clear_cookies()
            self.end_headers()
            self.wfile.write(b'Private!')
        elif self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    data = f.read()
                self.send_response(200)
                if clear == True:
                    self.clear_cookies()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_response(500)
                if clear == True:
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
                    if clear == True:
                        self.clear_cookies()
                    self.end_headers()
                    self.wfile.write(b'Forbidden')
            except Exception:
                self.send_response(500)
                if clear == True:
                    self.clear_cookies()
                self.end_headers()
                self.wfile.write(b'Error')
        elif os.path.isdir(path):
            try:
                self.send_response(200)
                if clear == True:
                    self.clear_cookies()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(str(os.listdir(path)).encode())
            except Exception:
                self.send_response(500)
                if clear == True:
                    self.clear_cookies()
                self.end_headers()
                self.wfile.write(b'error')
        else:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                if clear == True:
                    self.clear_cookies()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_response(500)
                if clear == True:
                    self.clear_cookies()
                self.end_headers()
                self.wfile.write(b'error')

    def do_POST(self):

        cookies = self.parse_cookies(self.headers['Cookie'])
        if sessions != {}:
            if cookies != None:
                if 'username' and 'sid' in cookies:
                    username = cookies['username']
                    if (cookies['sid'] in sessions[username]):
                        self.user = sessions[username]
                    else:
                        del sessions[username]
                        self.user = False
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

        if (self.path == '/create_post.json'):
            self.create_post()

    def generate_sid(self):
        return ''.join(str(randint(1,9)) for _ in range(100))

    def login(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(str(self.rfile.read(content_len), encoding='utf-8'))
        print('Request payload: ' + json.dumps(post_body))
        username = post_body['username']
        password = post_body['password']
        login_status = database.login_user(username, password)
        if login_status == 'SUCCESS':
            self.send_response(200)
            sid = self.generate_sid()
            self.cookies = ['sid={}'.format(sid), 'username='+username]
            for cookie in range(0, len(self.cookies)):
                self.send_header('Set-Cookie', self.cookies[cookie] + ';max-age=3600;path=/')
            sessions[username] = {'sid': sid, 'max-age': 3600}
            return_object = {'login': 'success'}
            print('login successful for ' + username)
        elif login_status == 'FAILURE':
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
        user_creation_status = database.create_user(username, password)
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
        username = post_body['username']
        if self.user == False or self.user != post_body['username']:
            return_object = {'post_creation': 'failure'}
            self.send_response(403)
            print('unauthorised access attempt by ' + username)
        else:
            headline = post_body ['headline']
            content = post_body['content']
            post_creation_status = database.create_post(username, headline, content)
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

httpd = socketserver.TCPServer(('', PORT), MyHandler)
print('Server started on ', PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print('Server stopped.')