import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os

PathImages = "D:\MS_Related\ASU\CSE598_Robotics\LearningOpenCV4\images"
absolute_path = os.path.dirname(__file__)
# relative_path = "CameraAndVision\Images"
relative_path = "Images\\new-setup-images"
OutputImageNew = os.path.join(absolute_path, "Images\OutputNew")

#Try Chapter3
def TryContourDetection():
    #create an image
    img = np.zeros((200,200) , dtype=np.uint8)

    #place white square in the center 
    img[50:150,50:150] = 255
    cv2.imshow("Img1" ,img)

    #threshold the image
    ret, threshold = cv2.threshold(img, 127,255,0)
    cv2.imshow("Threshold1" ,threshold)
    #findContours - inputs - img, hierarchy type, contour approx method
        #cv2.RETR_EXTERNAL --objects appera on plain bckgnd
        #cv2.RETR_TREE -- retrieve entire hierarchy 
    contours, hierarchy = cv2.findContours(threshold , cv2.RETR_TREE , 
                                           cv2.CHAIN_APPROX_SIMPLE)
    
    print(type(contours)) #type is tuple
    print(contours) #tuple of array of rectangle dimensions 
    #convert to color image
    color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    #draw green contours on each of the contours/shapes found
    img = cv2.drawContours(color, contours, -1, (0,255,0), 2)
    cv2.imshow("contours", color)
    cv2.waitKey()
    cv2.destroyAllWindows()

def DetectLines():
    pathImg = PathImages + "\lines.jpg"
    img = cv2.imread(pathImg)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 120)
    minLineLength = 20
    maxLineGap = 5
    lines = cv2.HoughLinesP(edges, 1, np.pi/180.0, 20, minLineLength, maxLineGap)

    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)

def DetectCircles():
    # planets = cv2.imread('planet_glow.jpg')
    planets = cv2.imread(PathImages + "\planet_glow.jpg")
    gray_img = cv2.cvtColor(planets, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.medianBlur(gray_img, 5)
    circles = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,120,
        param1=100,param2=30,minRadius=0,maxRadius=0)
    print(circles.shape)
    print(circles)
    circles = np.uint16(np.around(circles))
    print("========")
    print(circles)
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(planets,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(planets,(i[0],i[1]),2,(0,0,255),3)

    cv2.imwrite(OutputImageNew + "\\planets_circles.jpg", planets)
    cv2.imshow("HoughCirlces", planets)
    cv2.waitKey()
    cv2.destroyAllWindows()    

if __name__ == "__main__":
    # TryContourDetection()
    DetectCircles()
