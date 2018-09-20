#import libraries  
import cv2
from time import sleep
from picamera import PiCamera

# initializing camera
camera = PiCamera()
# adjust resolution and frame rate
camera.resolution = (320,240)
camera.framerate = 10
# record a video to the file
camera.start_preview()
camera.start_recording('/home/pi/video.h264')
camera.wait_recording(5)
camera.stop_recording()
camera.stop_preview()

# capture frames from stored video 
cap = cv2.VideoCapture('video.h264')
# initialize car counter
totalCount = 0
# XML classifier trained to detect cars
car_cascade = cv2.CascadeClassifier('cars.xml')

file = open("carFile.txt", "w+")
frameCount = 0

while True:
    # reads frames from a video
    ret, frames = cap.read()
    
    frameCount+=1
    
    # convert each frame to gray scale for processing
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    # Detects cars of different sizes
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    # car counter initalized in loop
    counter=0
    # places border lines on the image
    cv2.line(frames, (0, 180), (300,180),(255,0,0),2)
    cv2.line(frames, (0, 190), (300,190),(0,255,0),2)
    # To draw a dot in the bottom right corner of each car
    for (x,y,w,h) in cars:
        cv2.rectangle(frames,(x+w,y+h),(x+w,y+h),(0,0,255),2)
        # if the car's dot passes between the lines, count it
        if y+h>=180 and y+h<=190:
            counter+=1
        
        # Display frames in a window 
        #cv2.imshow('video2', frames)
    totalCount+=counter
    file.write(str(totalCount) + "," + str(frameCount) + "\n")
    # display final car count
    #cv2.putText(frames,str(totalCount), (50,50), cv2.CV_FONT_HERSHEY_SIMPLEX, 2, 255)
    
    # Wait for Esc key to stop
    if cv2.waitKey(33) == 27:
        break

#file.write(totalCount + " cars in " + (frameCount/10) + " seconds.")
file.close()
# De-allocate any associated memory usage
cv2.destroyAllWindows()


