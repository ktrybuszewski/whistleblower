import api
import requests
import os
import cv2
import numpy as np
from ultralyticsplus import YOLO, render_result
import time
from datetime import datetime, timedelta

model = YOLO('keremberke/yolov8s-hard-hat-detection')
falling_model = YOLO('yolov8s.pt')

model.overrides['conf'] = 0.25 
model.overrides['agnostic_nms'] = False 
model.overrides['max_det'] = 1000 

def detect_helmet_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    white_count = cv2.countNonZero(mask_white)
    yellow_count = cv2.countNonZero(mask_yellow)
    blue_count = cv2.countNonZero(mask_blue)
    if white_count > yellow_count and white_count > blue_count:
        color = 'WHITE'
    elif yellow_count > blue_count:
        color = 'YELLOW'
    elif blue_count > 0:
        color = 'BLUE'
    else:
        color = None  
    return color

def hardhat_processing(image_path):
    frame = cv2.imread(image_path)
    alert_label = ""
    if frame is None:
        print("Error: Could not read the image.")
        return False
    results = model.predict(frame)
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        label = model.names[class_id]
        if label == 'Hardhat':
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            helmet_region = frame[y1:y2, x1:x2]
            helmet_color = detect_helmet_color(helmet_region)
            if helmet_color in ['WHITE', 'YELLOW', 'BLUE']:
                cv2.putText(frame, f'Kolor: {helmet_color}', (x1, y1 - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if label == 'NO-Hardhat':
            alert_label = " NO HARDHAD DETECTION "
    return alert_label 

def falling_detecting(frame):
    alert_label = ""
    results = falling_model.predict(frame)
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls[0])
        label = falling_model.names[class_id] 

        if label == 'person':
            width = x2 - x1
            height = y2 - y1
            if (height*2.5) < width:
                alert_label = " FALL DETECTED"
    return alert_label

count = 0
cutofftime = datetime.now()
hoursofffset = 2
cutofftimeoffset  = cutofftime - timedelta(hours = hoursofffset)
timestamp = cutofftimeoffset.strftime('%Y%m%d%H%M%S%f')[:16]

while True:
    photos_data = api.get_photos(10, timestamp)
    for data in photos_data:
        with open(data[0], 'wb') as f:
            resp = requests.get(data[1], verify=False)
            f.write(resp.content)
            alert1 = hardhat_processing(data[0])
            alert2 = falling_detecting(data[0])
            alert = alert1 + alert2
            count = count + 1 
            print(count)
            timestamp = data[2]
            if alert != "":
                print(str(data[0]) + "  "+ alert)
                api.set_alert(data[2], alert)

            else: 
                print(str(data[0]) + "  NO ALERT")

        try:
            os.remove(data[0])
            
        except OSError as e:
            print(f"Nie można usunąć pliku {data[0]}: {e}")
cv2.destroyAllWindows()
