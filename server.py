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
        if (self.path == "/login.json"):
            content_len = int(self.headers.get('Content-Length'))
            post_body = json.loads(str(self.rfile.read(content_len), encoding="utf-8"))
            print("Request payload: " + json.dumps(post_body))
            username = post_body['username']
            password = post_body['password']
            login_status = database.check_user(username, password)
            if login_status == 'SUCCESS':
                return_string = 'Login Successful\n'
                self.send_response(200)
            else:
                return_string = 'Login Failed\n'
                self.send_response(403)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(return_string), encoding="utf-8"))
        if (self.path == "/create_user.json"):
            content_len = int(self.headers.get('Content-Length'))
            post_body = json.loads(str(self.rfile.read(content_len), encoding="utf-8"))
            print("Request payload: " + json.dumps(post_body))
            username = post_body['username']
            password = post_body['password']
            user_creation_status = database.create_user(username, password)
            if user_creation_status == 'SUCCESS':
                return_string = 'User Creation Successful\n'
                self.send_response(200)
            else:
                return_string = 'User Creation Failed\n'
                self.send_response(409)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(return_string), encoding="utf-8"))

httpd = socketserver.TCPServer(("", PORT), MyHandler)
print("Server started on ", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print("Server stopped.")