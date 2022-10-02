import numpy as np
import cv2
import time
from control_arduino import func

# cap the video from the pc cam
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

ret1, img1 = vid.read()
resized_img1 = cv2.resize(img1,(600,400))

ret2, img2 = vid.read()
resized_img2 = cv2.resize(img2,(600,400))
led_state = 'LED OFF'

old_time = time.time()

while True:
    
    diff = cv2.absdiff(resized_img1, resized_img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 900:
            continue
            

        else:
            # else there is a movement
            cv2.rectangle(resized_img1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(resized_img1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # turn on led for 10 seconds then turn off
            if led_state == 'LED OFF':
                led_state = 'LED ON'
            else:
                led_state = 'LED OFF'
            func(led_state)
        
        time.sleep(10)
        if led_state == 'LED ON':
            func('LED OFF')
            led_state = 'LED OFF'
            break
            
    
    # new_time = time.time()
    # if new_time - old_time >= 9:
    #     break

    time.sleep(5)

    image = cv2.resize(resized_img1, (1280,720))
    cv2.imshow("feed", resized_img1)
    
    resized_img1 = resized_img2
    
    ret2, img2 = vid.read()
    resized_img2 = cv2.resize(img2,(600,400))
    
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

    
cv2.destroyAllWindows()