import cv2
import numpy as np

# Open a connection to the camera (0 represents the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to identify black pixels
    _, thresholded = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # Find contours of black pixels
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of black pixels
    black_pixel_count = 0

    for contour in contours:
        # Calculate the area of each contour
        area = cv2.contourArea(contour)
        
        # Consider contours with a minimum area to filter out noise
        if area > 10:
            # Draw a green circle around the black pixel
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
            black_pixel_count += 1

    # Print the count
    print("Black Pixel Count:", black_pixel_count)

    # Save the frame with a green circle as a JPEG image
    cv2.imwrite("black_pixel_image.jpg", frame)

    # Exit when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()

