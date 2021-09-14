#!/usr/bin/python

from http import server
from http.server import BaseHTTPRequestHandler,HTTPServer
import movementControl
import threading
from time import sleep

serverPort = 8081

class Robot_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            movementControl.spinMode()
            sleep(1)

turretMode = "false"
thread = Robot_thread()
prev = 0

class connectionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
        except KeyboardInterrupt:
            pass
    def do_POST(self):
        global turretMode
        global thread
        global prev
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        leftJoy, rightJoy, turretMode = movementControl.decodeHTTPData(post_data)
        if(turretMode == "false"):
            if(prev == 1):
                thread.event.set()
            movementControl.setMotorSpeed(leftJoy, rightJoy)
            prev = 0
        else:
            if(prev == 0):
                thread = Robot_thread()
                thread.start()
            prev = 1
        try:
            self.send_response(200)
        except KeyboardInterrupt:
            pass
    
def main():
    try:
        server = HTTPServer(('', serverPort), connectionHandler)
        print("Data exchange server started")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Date exchange server closed")
        server.socket.close()
        

if __name__ == '__main__':
    main()
