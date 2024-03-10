import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import psutil

# Function to print system resource usage
def print_resource_usage():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()

    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_info.percent}%")

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warmup
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Print system resource usage
    print_resource_usage()

    # Rest of your code

    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # Add a delay to achieve the desired frame rate
    time.sleep(1 / 30)
