import cv2 #importing the opencv library for image or video processing 
import imutils #importing the imutils library for image processing(resize the image)

camera = cv2.VideoCapture(0) #camera access panna 
first_frame = None
area =500 #Focused on the objects which is bigger than this value 
while True:
    _,img=camera.read() #reading the image from the camera
    text ="Relax Movement Not Found"
    img = imutils.resize(img,width=1000) #used for resizing the image
    grayImg =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Colorful image ah Gray image ah mathurom
    gaussianImg = cv2.GaussianBlur(grayImg,(21,21),0) #used for blurring the image with the help of gaussian filter
    if first_frame is None:
        first_frame = gaussianImg
        continue
    imgDiff = cv2.absdiff(first_frame,gaussianImg) #used for finding the difference between the first frame and the current frame, also to identify which object comes within the frame newly
    thresholdImg = cv2.threshold(imgDiff,20,255,cv2.THRESH_BINARY)[1] #used for thresholding the image
    thresholdImg = cv2.dilate(thresholdImg,None,iterations=3) #used for dilating the image, Used for filling the holes or gaps
    cnts = cv2.findContours(thresholdImg.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #used for finding the contours
    cnts = imutils.grab_contours(cnts) #Used to grab all the contors into one list
    for c in cnts:
        if cv2.contourArea(c)<area:
            continue
        (x,y,w,h) =cv2.boundingRect(c) #used for finding the rectangle around the object
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2) #used for drawing the rectangle around the object
        text = "Movement Found"
    print(text)
    cv2.putText(img,text,(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2) #Used for displaying the text within the image 
    cv2.imshow("camera feed",img)
    key = cv2.waitKey(10)
    print(key)
    if key == ord("g"):
        break

camera.release()
cv2.destroyAllWindows()