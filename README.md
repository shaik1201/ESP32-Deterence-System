# cats_detection

Identify and notify when cats enter my yard so i would be able to prevent them from defecating there. Using python with opencv.


- track cats movement in the yard, record the time and notify me through an email.
- after trcaking the movement, turn on a spinkler to keep the cats away.
- Use arduino/esp32 board. (currently using an old laptop to run the script in real time).

UPDATE:
Currently controling the arduino using http request to turn a sprinkler on/off. (just_cv.py).
