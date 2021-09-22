#!/usr/bin/env python3

import http.server
import json
import os
import socketserver
from modules import database

PORT = 8080

database.create_tables()

serve_from = os.getcwd()

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = serve_from + self.path
        print(self.path)
        if not os.path.abspath(path).startswith(serve_from):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Private!')
        elif self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'error')
        elif os.path.isdir(path):
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str(os.listdir(path)).encode())
            except Exception:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'error')
        else:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'error')
    def do_POST(self):
        print(self.path)

        if (self.path == '/login.json'):
            content_len = int(self.headers.get('Content-Length'))
            post_body = json.loads(str(self.rfile.read(content_len), encoding='utf-8'))
            print('Request payload: ' + json.dumps(post_body))
            username = post_body['username']
            password = post_body['password']
            login_status = database.login_user(username, password)
            print(login_status)
            if login_status == 'SUCCESS':
                return_object = {'login': 'success'}
                self.send_response(200)
                print('login successful for ' + username)
            elif login_status == 'FAILURE':
                return_object = {'login': 'failure'}
                self.send_response(403)
                print('login failed for ' + username)
            else:
                return_object = {'login': 'error'}
                self.send_response(500)
                print('login error for ' + username)

            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(str(json.dumps(return_object)), encoding='utf-8'))

        if (self.path == '/create_user.json'):
            content_len = int(self.headers.get('Content-Length'))
            post_body = json.loads(str(self.rfile.read(content_len), encoding='utf-8'))
            print('Request payload: ' + json.dumps(post_body))
            username = post_body['username']
            password = post_body['password']
            user_creation_status = database.create_user(username, password)

            if user_creation_status == 'SUCCESS':
                return_object = {'user_creation': 'success'}
                self.send_response(200)
                print('user creation successful for ' + username)
            elif user_creation_status == 'FAILURE':
                return_object = {'user_creation': 'failure'}
                self.send_response(409)
                print('user creation failed for ' + username)
            else:
                return_object = {'user_creation': 'error'}
                self.send_response(500)
                print('user creation error for ' + username)

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