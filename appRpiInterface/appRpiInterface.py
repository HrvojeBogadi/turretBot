#!/usr/bin/python

from http import server
from http.server import BaseHTTPRequestHandler,HTTPServer
import movementControl

serverPort = 8081

class connectionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
        except KeyboardInterrupt:
            pass
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        movementControl.decodeHTTPData(post_data)
        try:
            self.send_response(200)
        except KeyboardInterrupt:
            pass
    
def main():
    global start
    try:
        server = HTTPServer(('', serverPort), connectionHandler)
        print("Data exchange server started")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Date exchange server closed")
        server.socket.close()

if __name__ == '__main__':
    main()
