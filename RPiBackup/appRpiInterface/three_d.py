import cv2
import numpy as np
import yolo
from openni import openni2
from openni import _openni2 as c_api

def get_angles():
    n = 0
    xp, yp = (0,0)
    net = cv2.dnn.readNetFromDarknet("yolov4-tiny-custom.cfg", "yolov4-tiny-custom_best.weights")

    path = "/home/pi/Downloads/AstraSDK-v2.1.2-89d64f5b3c-20210226T030351Z-Linux-arm/lib/Plugins/openni2"
    openni2.initialize(path)
    dev = openni2.Device.open_any()
    dev.set_depth_color_sync_enabled(1)

    depth = dev.create_depth_stream()
    rgb = dev.create_color_stream()

    depth.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 320, resolutionY = 240, fps = 30))
    rgb.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=320, resolutionY=240, fps=30))

    depth.start()
    rgb.start()

    cx = 158.487901371659
    cy = 124.386871654645
    fx = 253.283938852568
    fy = 254.067391233647

    while(xp < 0.001 and yp < 0.001):
        color = rgb.read_frame()
        frame = depth.read_frame()
    
        color_data = color.get_buffer_as_uint8()
        color_img = np.frombuffer(color_data, dtype=np.uint8)
        color_img.shape = (240, 320, 3)
        color_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB)

        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)
        img.shape = (1, 240, 320)
        img = np.concatenate((img, img, img), axis=0)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)

        _, xp, yp = yolo.get_output_image(color_img, net)
        n = n+1
        if(n > 4):
            return ('n',0)
        z = img[yp, xp][0]
        x = (xp - cx) * z / fx
        y = (cy - yp) * z / fy

        alpha = -25 * np.pi/180
        s_alpha = np.sin(alpha)
        c_alpha = np.cos(alpha)
    
        T1 = np.array([[1,0,0,-50],[0,c_alpha,-s_alpha,65],[0,s_alpha,c_alpha,-60],[0,0,0,1]])
        T2 = np.array([[1,0,0,-35],[0,c_alpha,-s_alpha,70],[0,s_alpha,c_alpha,-65],[0,0,0,1]])
        p = np.array([x,y,z,1])
        pp1 = np.matmul(T1, p)
        pp2 = np.matmul(T2, p)

        x, y, z,_ = pp1

        theta = np.arcsin(x/np.sqrt(z**2+x**2)) * 180/np.pi

        x, y, z,_ = pp2

        phi = np.arcsin(y/np.sqrt(z**2+y**2)) * 180/np.pi
        print("3d pass")

    openni2.unload()
    return (theta,phi)
