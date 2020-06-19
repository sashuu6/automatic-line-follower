import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from imutils.video import VideoStream

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module

cascPath = "stop_haar.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

# Uncomment line 14 and comment line 13 for PiCam
video_capture = cv2.VideoCapture(0)
# video_capture = VideoStream(usePiCamera=True).start()
anterior = 0

stopPin = 5
GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
# Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(stopPin, GPIO.OUT, initial=GPIO.LOW)

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print("Stop sign detected!!")
        GPIO.output(stopPin, GPIO.HIGH)  # Turn on
        sleep(1)  # Sleep for 1 second
        GPIO.output(stopPin, GPIO.LOW)  # Turn off
        sleep(1)  # Sleep for 1 second

    if anterior != len(faces):
        anterior = len(faces)
        log.info("Stop signed detected: "+str(len(faces)) +
                 " at "+str(dt.datetime.now()))

    # Display the resulting frame
    # cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    # cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
