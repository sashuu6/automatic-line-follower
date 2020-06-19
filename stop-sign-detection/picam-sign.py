import io
import picamera
import cv2
import numpy

import RPi.GPIO as GPIO
import time

switch = 11

# Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch, GPIO.IN)
# Get the picture (low resolution, so it should be quite fast)
# Here you can also specify other parameters (e.g.:rotate the image)
with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.capture(stream, format='jpeg')

# Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

# Now creates an OpenCV image
image = cv2.imdecode(buff, 1)

# Load a cascade file for detecting signs
sign_cascade = cv2.CascadeClassifier('stop_haar.xml')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Look for signs in the image using the loaded cascade file
signs = sign_cascade.detectMultiScale(gray, 1.1, 5)

print("Found "+str(len(signs))+" sign(s)")

if signs:
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(led, GPIO.LOW)

# Draw a rectangle around every found sign
for (x, y, w, h) in signs:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)

# Save the result image
cv2.imwrite('result.jpg', image)
