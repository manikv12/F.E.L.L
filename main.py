import cv2
import time

capture = cv2.VideoCapture('video1.MOV')
time.sleep(2)

# Ensures the video is set for 1080p
try:
    capture.set(3, 1920)
    capture.set(4, 1080)
except:
    print("camera resolution not accepted")

# Detect the moving part in the image and remove the still background
backSubtractor = cv2.createBackgroundSubtractorKNN(detectShadows=False)
counter = 0

while(True):
    #Convert the video into the frames
    ret, frame = capture.read()
    
    #Convert all the frame to gray scale and subtract the background
    try:
        blured_frame = cv2.GaussianBlur(frame,(1,1),cv2.BORDER_DEFAULT)
        gray = cv2.cvtColor(blured_frame, cv2.COLOR_BGR2GRAY) # Convert the image to grayscale
        fgmask = backSubtractor.apply(gray)  #background subtraction
        
        #Find contours of the object that is stored as foregroundmask in variable fgmask
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
        
            # A list that will hold areas of all the moving objects in the frames
            areas = []
            #Get area of all moving object in the frame and then append it
            for contour in contours:
                area = cv2.contourArea(contour)
                areas.append(area)
            
            #Find the object with the maximum area in the array that would be considered as human
            maxArea = max(areas, default = 0)
            maxAreaIdx = areas.index(maxArea) #index of object with maximum area
            
            # Get the object with the maximum area   
            human = contours[maxAreaIdx]
            
            #Draw contours against the object in masked image
            cv2.drawContours(fgmask, [human], 0, (129,255,0), 10, maxLevel = 1)
            
            # Make a rectangle around the object with maximum area .
            x, y, w, h = cv2.boundingRect(human)

            
            #If the height of the counters of the object is less than width
            if maxArea > 2500: #If the area of the mask is greater than this then only there is human
                if h < w:
                    counter += 1
            
                if counter > 17:
                    cv2.putText(frame, 'Fall Detected', (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

                #If the person stands up again
                if h > w:
                    counter = 0 
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


            cv2.imshow('F.E.L.L', frame)
            cv2.imshow('Maksed',fgmask)

            if cv2.waitKey(33) == ord('q'):
                break
    except:
        break
cv2.destroyAllWindows()
