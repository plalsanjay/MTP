#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2,time
import numpy as np

def fill_holes(imInput, threshold):
    """
    The method used in this function is found from
    https://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/

    """

    # Threshold.
    th, thImg = cv2.threshold(imInput, threshold, 255, cv2.THRESH_BINARY_INV)

    # Copy the thresholded image.
    imFloodfill = thImg.copy()

    # Get the mask.
    h, w = thImg.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Floodfill from point (0, 0).
    cv2.floodFill(imFloodfill, mask, (0,0), 255)

    # Invert the floodfilled image.
    imFloodfillInv = cv2.bitwise_not(imFloodfill)

    # Combine the two images.
    imOut = thImg | imFloodfillInv

    return imOut
#global bg
video = cv2.VideoCapture("/Users/sanjayplal/Downloads/IMG_0978.mov")
first_frame=None
fgbg = cv2.createBackgroundSubtractorMOG2(10,25,detectShadows = False)
z =0
count =0
while True:
    check,frame =video.read()
    if check !=True:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame,0)
    fgmask = fgbg.apply(frame,0.9)
    #blurred = cv2.GaussianBlur(fgmask, (11, 11), 0)
    #filled = fill_holes(blurred, 220)

    kernelsize = np.ones((3, 3), np.uint8)
    fgmask = cv2.dilate(fgmask,kernelsize,iterations=1)
    #fgmask = cv2.absdiff(bg.astype("uint8"), fgmask)
    contours, hierarchy  = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(type(contours))
    x =0
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area>100 and area <300:
            x = x+area
            cv2.drawContours(fgmask, contours, i, (0,255,75), 2)
    print(x)
    if area >500:
        flag=True
    if area<350:
        count = count+1
    if count>30:
        flag=False
    if flag==True:
        z = z+1
    if area>400 and count!=0:
        count=0

    #fgmask = cv2.adaptiveThreshold(fgmask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #kernelsize = np.ones((2, 2), np.uint8)
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelsize)
    #fgmask = cv2.dilate(fgmask,kernelsize,iterations=1)
    #cv2.imshow("cvghj",frame)
    cv2.imshow("cvgh",fgmask)
    key=cv2.waitKey(5)
    if key ==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
print(z/60," seconds")
    


# In[ ]:





# In[ ]:





# In[ ]:




