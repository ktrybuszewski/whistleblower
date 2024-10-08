from ultralyticsplus import YOLO, render_result
import cv2
import numpy as np
import time
cap = cv2.VideoCapture(0)

model = YOLO('keremberke/yolov8s-hard-hat-detection')
falling_model = YOLO('yolov8s.pt')
model.overrides['conf'] = 0.25 
model.overrides['iou'] = 0.45 
model.overrides['agnostic_nms'] = False 
model.overrides['max_det'] = 1000 
desired_fps = 10
frame_interval = 1 / desired_fps 
last_time = time.time()

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

def hardhat_processing(frame):
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
            cv2.putText(frame, f'NO HARDHAT DETECTION', (40, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    render = render_result(model=model, image=frame, result=results[0])
    if isinstance(render, np.ndarray):
        render_image = render
    else:
        render_image = np.array(render)
    cv2.imshow('Hard Hat Detection', render_image)

def falling_detecting(frame):
    results = falling_model.predict(frame)
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls[0])
        label = falling_model.names[class_id]
        if label == 'person':
            width = x2 - x1
            height = y2 - y1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if (height*2.5) < width:
                cv2.putText(frame, f'FALLING DETECTION', (40, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.imshow('Fall Detection', frame)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    current_time = time.time()
    if current_time - last_time >= frame_interval:
        last_time = current_time
        hardhat_processing(frame)
        falling_detecting(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

