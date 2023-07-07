import cv2,time
import numpy as np

def empty(a):
    pass
    
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,False)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)


            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)


cv2.namedWindow('parameter')
cv2.resizeWindow('parameter',640,240)
cv2.createTrackbar('hue min','parameter',0,179,empty)
cv2.createTrackbar('hue max','parameter',0,179,empty)
cv2.createTrackbar('sat min','parameter',0,255,empty)

cv2.createTrackbar('sat max','parameter',255,255,empty)
cv2.createTrackbar('value min','parameter',0,255,empty)
cv2.createTrackbar('value max','parameter',255,255,empty)



def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


video = cv2.VideoCapture("/home/kaushal/Desktop/Videosss/20220122_184557.mp4")

#first_frame=None
#fgbg = cv2.createBackgroundSubtractorMOG2(5,25,detectShadows = False)
#z =0
#count =0

x,y =210,506
w,h = 420,420

#imgContour =frame.copy()
while True:
    check,frame =video.read()
    frame = frame[y:y+h, x:x+w]
    # Show image
    
    #if check !=True:
      #  break
    #code for color detection using trackbars and after converting image into hsv
    #imgblur = cv2.GaussianBlur(frame,(1,1),4)
    imghsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    
    t1 = cv2.getTrackbarPos('hue min','parameter')
    t2 = cv2.getTrackbarPos('hue max','parameter')
    t3 = cv2.getTrackbarPos('sat min','parameter')
    t4 = cv2.getTrackbarPos('sat max','parameter')
    t5 = cv2.getTrackbarPos('value min','parameter')
    t6 = cv2.getTrackbarPos('value max','parameter')
    lower = np.array([t1,t3,t5])
    upper = np.array([t2,t4,t6])
    
    mask = cv2.inRange(imghsv,lower,upper)
    
    #imgblur = cv2.GaussianBlur(mask,(1,1),4)
        
    # Convert the image to grayscale
    #h, s, v1 = cv2.split(imgblur)
    #imgcanny = cv2.Canny(imgblur,50,50)
    #getContours(imgcanny)
    #cv2.imshow('frame',frame)
    #cv2.imshow('hsv',imghsv)
    cv2.imshow('mask',mask)
    
    # Find contours of the red areas
    
    #cv2.waitKey(1000000)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
