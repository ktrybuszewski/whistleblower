import numpy as np
import cv2 as cv
import Person
import time
import api


cnt_up = 0
cnt_down = 10

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)



h = 480
w = 640
frameArea = h * w
areaTH = frameArea / 250  # Ustalony próg obszaru
print('Area Threshold:', areaTH)

# Linie wejścia/wyjścia
line_up = int(1.5 * (h / 5))
line_down = int(2.5 * (h / 5))
up_limit = int(1 * (h / 5))
down_limit = int(4 * (h / 5))


line_down_color = (255, 0, 0)
line_up_color = (0, 0, 255)


pts_L1 = np.array([[0, line_down], [w, line_down]], np.int32).reshape((-1, 1, 2))
pts_L2 = np.array([[0, line_up], [w, line_up]], np.int32).reshape((-1, 1, 2))
pts_L3 = np.array([[0, up_limit], [w, up_limit]], np.int32).reshape((-1, 1, 2))
pts_L4 = np.array([[0, down_limit], [w, down_limit]], np.int32).reshape((-1, 1, 2))


fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)


kernelOp = np.ones((3, 3), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)

# Zmienne
font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

previous_people = 0


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print('Koniec pliku wideo lub błąd.')
        break

    for person in persons:
        person.age_one()

    fgmask = fgbg.apply(frame)

    try:
        ret, imBin = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)
        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print('UP:', cnt_up)
        print('DOWN:', cnt_down)
        break

    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > areaTH:
            M = cv.moments(cnt)
            if M['m00'] == 0:
                continue
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv.boundingRect(cnt)

            new = True
            if up_limit < cy < down_limit:
                for person in persons:
                    if abs(x - person.getX()) <= w and abs(y - person.getY()) <= h:
                        new = False
                        person.updateCoords(cx, cy)
                        if person.going_UP(line_down, line_up):
                            cnt_up += 1
                            print(f"ID: {person.getId()} crossed going up at {time.strftime('%c')}")
                        elif person.going_DOWN(line_down, line_up):
                            cnt_down += 1
                            print(f"ID: {person.getId()} crossed going down at {time.strftime('%c')}")
                        break

                    if person.getState() == '1':
                        if person.getDir() == 'down' and person.getY() > down_limit:
                            person.setDone()
                        elif person.getDir() == 'up' and person.getY() < up_limit:
                            person.setDone()

                    if person.timedOut():
                        persons.remove(person)
                        del person

                if new:
                    p = Person.MyPerson(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1

            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    str_up = f'UP: {cnt_up}'
    str_down = f'DOWN: {cnt_down}'
    people = cnt_down - cnt_up

    if people != previous_people:
        api.send_to_api(people)  
        previous_people = people  

    frame = cv.polylines(frame, [pts_L1], False, line_down_color, thickness=4)
    frame = cv.polylines(frame, [pts_L2], False, line_up_color, thickness=4)

    cv.putText(frame, "Entrance to the construction site ", (20, 440), font, 0.5, (255, 0, 0), 1, cv.LINE_AA)
    start_point = (350, 420)  
    end_point = (350, 460)    
    cv.arrowedLine(frame, start_point, end_point, (255, 0, 0), 2, tipLength=0.3)  

    cv.putText(frame, ("Number of people on the construction site  " + str(people)), (10, 400), font, 0.6, (255, 0, 0), 2, cv.LINE_AA)

    cv.imshow('Frame', frame)

    if cv.waitKey(30) & 0xFF == 27:  
        break

cap.release()
cv.destroyAllWindows()
