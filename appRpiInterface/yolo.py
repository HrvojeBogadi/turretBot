import cv2
import numpy as np

net_def = cv2.dnn.readNetFromDarknet("yolov4-tiny-custom.cfg", "yolov4-tiny-custom_best.weights")

def get_output_image(img, net=net_def):
    image = img.copy()
    
    (H, W) = image.shape[:2]

    min_confidence = 0.5

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(ln)

    boxes = []
    centers = []
    confidences = []

    for output in outputs:
        for detection in output:
            confidence = detection[5]
            if confidence > min_confidence:
                box = detection[0:4] * np.array([W, H, W, H])
                (c_x, c_y, w, h) = box.astype("int")
                x = int(c_x - (w / 2))
                y = int(c_y - (h / 2))
                centers.append([c_x, c_y])
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))

    c_x, c_y = [0,0]

    if(len(confidences) > 0):
        i = np.argmax(confidences)
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        c_x, c_y = centers[i]
        color = (255,0,0)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            
    return (image, c_x, c_y)
