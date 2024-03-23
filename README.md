import cv2, time
import numpy as np

# Function to dynamically adjust the threshold based on the local mean and standard deviation
def adaptive_threshold(image, k_size=25, offset=10):
    blurred = cv2.GaussianBlur(image, (k_size, k_size), 0)
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, k_size, offset)
    return thresholded
# Setup SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()

# Filter by Area.
params.filterByArea = True
params.minArea = 15  # Adjust this value based on the size of the objects you want to detect

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

video = cv2.VideoCapture(0 + cv2.CAP_VFW)

video.set(cv2.CAP_PROP_FPS, 90)

frame_width = 1920
frame_height = 1080

xy_list = []
bounding_list = []
contour_list = []

prev_frame_time = 0
new_frame_time = 0
second = 0
totalFrame = 0
prev_contour = 0
lastCoordinate = 0
staticFrame = 0

# Tracking Sensitivity (lower = more sensitive)
sensitivity = 45

# List when any moving object appear
motion_list = [None, None]
static_back = None

font = cv2.QT_FONT_NORMAL
        
while True:
    totalFrame +=1
    
    check, frame = video.read()
    
    try:
        #frame = cv2.resize(frame, (frame_width, frame_height))
        motion = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        time.sleep(0.001)
        break

    # Converting gray scale image to GaussianBlur
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    gray = cv2.blur(gray, (5, 5))

    # Assign value of static_back for the first time
    if static_back is None:
        static_back = gray
        continue
    
    # Difference between static background
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray) 
    # diff_frame = cv2.dilate(diff_frame, np.ones((10, 10)), 1)

    # If change in between static background and
    # current frame is greater than (sensitivity var) it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, sensitivity, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, np.ones([20, 20]), iterations=6)

    # Finding contour of moving object
    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if (cv2.contourArea(contour) > 10000):
            motion = 1
            contour_list.append(cv2.contourArea(contour))
            (x, y, w, h) = cv2.boundingRect(contour)
            bounding_list.append([x, y, w, h])
            xy_list.append(int((x+(w/2))*(y+(h/2))))

        else:
            continue

        # making green rectangle around the moving object
   
    if len(contour_list) != 0:
        # Finding the closest contour compared to previous x and y contour's coordinate
        prev_contour = min(xy_list, key=lambda a:abs(a-prev_contour))
        
        # Display all contours
        #for bounding in bounding_list:
        #    (x, y, w, h) = (bounding)
        #    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
          
        (x, y, w, h) = (bounding_list[xy_list.index(prev_contour)])
        cv2.putText(frame, str(w*h), (x+20, y+30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=3)
      
        print(f"Area({len(xy_list)}) : " + str(xy_list))
        print(f"x : {x} | y : {y}\n")

    # Calculating the fps
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)

    if fps > 20:
        cv2.putText(frame, str(fps) + "/" + str(len(xy_list)), (5, 20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    elif (fps <= 20) & (fps >= 10):
        cv2.putText(frame, str(fps) + "/" + str(len(xy_list)), (5, 20), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    else:
        cv2.putText(frame, str(fps) + "/" + str(len(xy_list)), (5, 20), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        
    # Threshold the image to identify dark objects
    thresholded = adaptive_threshold(diff_frame)

    # Morphological operations to enhance blob detection
    kernel = np.ones((5, 5), np.uint8)
    morphed = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

    # Detect blobs.
    keypoints = detector.detect(morphed)
    
    # Find the biggest blob
    if keypoints:
        blob = max(keypoints, key=lambda x: x.size)
        x, y = blob.pt
        cv2.circle(frame, (int(x), int(y)), int(blob.size/2), (0, 255, 0), -1)

    # cv2.imshow("Gray Frame", gray)
    #cv2.imshow("Difference Frame", diff_frame)
    
    cv2.imshow("Color Frame", frame)
    print(fps)

    if len(xy_list) != 0:
        x,y = 0,0
        contour_list.clear()
        bounding_list.clear()
        xy_list.clear()

    static_back = gray

    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        video.release()
        time.sleep(0.001)

    continue

cv2.destroyAllWindows()
