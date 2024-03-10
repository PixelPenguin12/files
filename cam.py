import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pin = 13
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def angle_to_duty(angle):
    min_duty = 26
    max_duty = 128
    return (min_duty + (angle / 180.0) * (max_duty - min_duty)) / 10

# Setup SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()

# Filter by Area.
params.filterByArea = True
params.minArea = 7  # Adjust this value based on the size of the objects you want to detect

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)
# Open a connection to the camera (0 represents the default camera)
cap = cv2.VideoCapture(0)

# Set camera frame rate to 30fps
cap.set(cv2.CAP_PROP_FPS, 90)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

pwm.ChangeDutyCycle(angle_to_duty(45))
time.sleep(1)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to identify dark objects
    _, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Detect blobs.
    keypoints = detector.detect(thresholded)

    # Find the biggest blob
    if keypoints:
        blob = max(keypoints, key=lambda x: x.size)
        x, y = blob.pt
        cv2.circle(frame, (int(x), int(y)), int(blob.size/2), (0, 255, 0), -1)
        cent_x = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2
        cent_y = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) / 2
        x -= cent_x
        y -= cent_y
        pwm.ChangeDutyCycle(angle_to_duty(x/30))
    # Exit when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
