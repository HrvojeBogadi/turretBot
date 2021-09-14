#!/usr/bin/python

from http import server
from http.server import BaseHTTPRequestHandler,HTTPServer
import movementControl
import threading
import cv2
import io
import yolo
import three_d
import gpio
from time import sleep

serverPort = 8081

img = 0
net = cv2.dnn.readNetFromDarknet("yolov4-tiny-custom.cfg", "yolov4-tiny-custom_best.weights")

class Robot_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            _, x, y = yolo.get_output_image(img, net)
            if(x != 0 and y != 0):
                print("Found a person!")
                theta, phi = three_d.get_angles()
                gpio.shoot(theta, phi)
            movementControl.spinMode()

server_c = 0

class Camera_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        global server_c
        print("Camera server started")
        server_c.serve_forever()
        print("Ended")

cap = cv2.VideoCapture(0)
turretMode = "false"
thread = Robot_thread()
prev = 0

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global cap
        global img
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            stream=io.BytesIO()
            try:
                while(True):
                    ret, img = cap.read()
                    ret, jpg = cv2.imencode('.jpg', img)
                    # print 'Compression ratio: %d4.0:1'%(compress(img.size,jpg.size))
                    self.wfile.write("--jpgboundary".encode("utf-8"))
                    self.send_header('Content-type', 'image/jpeg')
                    # self.send_header('Content-length',str(tmpFile.len))
                    self.send_header('Content-length', str(jpg.size))
                    self.end_headers()
                    self.wfile.write(jpg.tostring())
                    sleep(0.05)
            except KeyboardInterrupt:
                pass
            return
        else:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("<html><head></head><body><img src='/cam.mjpg'/></body></html>", "utf8"))
            return


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
    global server_c
    try:
        server_c = HTTPServer(('',8080),CamHandler)
        cam_thread = Camera_thread()
        cam_thread.start()
        server = HTTPServer(('', serverPort), connectionHandler)
        print("Data exchange server started")
        server.serve_forever()
    except KeyboardInterrupt:
        cap.release()
        server_c.socket.close()
        print("Date exchange server closed")
        server.socket.close()
        

if __name__ == '__main__':
    main()
