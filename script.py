import numpy as np
import cv2
import requests
import smtplib
import os
from datetime import datetime
from flask import Flask
from pymongo import MongoClient
from pprint import pprint
import time
from control_arduino import func

import yaml
try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

except Exception as e:
    print('Error reading the config file')



# get the email address and password from env vars
# set EMAIL_PASS=czwiksvmijykljoy
# set EMAIL_ADD=shaikiko12@gmail.com

# EMAIL_ADD = os.environ.get('EMAIL_ADD')
# EMAIL_PASS = os.environ.get('EMAIL_PASS')

EMAIL_ADD = config['smtp']['EMAIL_ADD']
EMAIL_PASS = config['smtp']['EMAIL_PASS']

# create new db to store the times cats are detected
client = MongoClient('localhost', 27017)
db = client.flask_db
cats = db.cats

# cap the video from the pc cam
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

ret1, img1 = vid.read()
resized_img1 = cv2.resize(img1,(600,400))

ret2, img2 = vid.read()
resized_img2 = cv2.resize(img2,(600,400))

  
sent_email = False
inserted_to_db = False
oldtime = time.time()

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
            
        # else there is a movement
        cv2.rectangle(resized_img1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(resized_img1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


        # send me an email
        if sent_email == False:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADD, EMAIL_PASS)
            
                subject = 'cat detected alert'
                body = f'cat detected at: {datetime.now()}'
                msg = f'subject: {subject} \n\n {body}'
            
                smtp.sendmail(EMAIL_ADD, EMAIL_ADD, msg)
                print('Email sent')
                
                sent_email = True
                
                
        # store time in the db
        # db.cats.delete_many( { } )
        if inserted_to_db == False:
            cats.insert_one({'time_detected':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            inserted_to_db = True
        
        if time.time() - oldtime >= 10*60: # if 10 minutes has passed, start checking again and insert to the db
            inserted_to_db = False
            oldtime = time.time()


        # turn on led
        func()
            
        
        
        
    image = cv2.resize(resized_img1, (1280,720))
    cv2.imshow("feed", resized_img1)
    
    resized_img1 = resized_img2
    
    ret2, img2 = vid.read()
    resized_img2 = cv2.resize(img2,(600,400))
    
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

        
# # store time in the db
# # db.cats.delete_many( { } )
# if inserted_to_db == False:
#     cats.insert_one({'time_detected':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
#     inserted_to_db = True        


# print the db content
cursor = cats.find({})
for document in cursor: 
    pprint(document)
    

cv2.destroyAllWindows()