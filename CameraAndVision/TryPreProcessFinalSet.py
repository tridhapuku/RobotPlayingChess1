import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os


absolute_path = os.path.dirname(__file__)
# relative_path = "CameraAndVision\Images"
relative_path = "Images\\new-setup-images"
OutputImageNew = os.path.join(absolute_path, "Images\OutputNew")
full_pathNewSet = os.path.join(absolute_path,relative_path)
Crop_hStart , Crop_hEnd = 40 , 970
Crop_wStart , Crop_wEnd = 310 , 1290

# Crop_hStartF , Crop_hEndF = 0, 0
# Crop_wStartF, Crop_wEndF = 0, 0

def GetImageProp():
    pathImg = full_pathNewSet + "\WIN_20230422_18_46_05_Pro.jpg"

    img = cv2.imread(pathImg)

    print(img.shape)

def TryCropOnFinalSet():
    NameImg = "WIN_20230422_18_46_05_Pro.jpg"
    pathImg = full_pathNewSet + "\\" + NameImg
    img = cv2.imread(pathImg)
    cropped_img = img[Crop_hStart:Crop_hEnd,Crop_wStart:Crop_wEnd]
    cv2.imshow("cropped" , cropped_img)
    cv2.imwrite(OutputImageNew + "\Cropped" +  NameImg, cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def DetectChessCorners():
    NameImg = "WIN_20230422_18_46_05_Pro.jpg"
    pathImg = OutputImageNew + "\\Cropped" + NameImg
    img = cv2.imread(pathImg)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('GrayImg',gray)
    cv2.imwrite(OutputImageNew + "\Gray1.jpg", gray)

    ret, corners = cv2.findChessboardCorners(gray,(7,7) , None)
    print("Finding chess board corners done")
    

    # return
    if ret == True:
        print(corners.shape)
        img = cv2.drawChessboardCorners(img, (7,7) , corners, ret)
        cv2.imshow('Chessboard', img)
        # cv2.waitKey(0)
        cv2.imwrite(OutputImageNew + "\ChessCorners1_7By78.png" , img)
    else:
        print("Chessboard Corners Not found!")

    cv2.destroyAllWindows()

def DetectContours():
    NameImg = "WIN_20230422_18_46_05_Pro.jpg"
    pathImg = OutputImageNew + "\\Cropped" + NameImg
    img = cv2.imread(pathImg)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('GrayImg',gray)
    
    #threshold the image
    ret, threshold = cv2.threshold(gray, 127,255,0)
    cv2.imshow("Threshold1" ,threshold)
    # cv2.imwrite(OutputImageNew + "\Threshold1.jpg", threshold)
    #findContours - inputs - img, hierarchy type, contour approx method
        #cv2.RETR_EXTERNAL --objects appera on plain bckgnd
        #cv2.RETR_TREE -- retrieve entire hierarchy 
    contours, hierarchy = cv2.findContours(threshold , cv2.RETR_CCOMP , 
                                           cv2.CHAIN_APPROX_SIMPLE)
    
    if(len(contours) > 0):
        print("len(contours)={} RETR_CCOMP".format(len(contours)))
        print("len(hierarchy)={} RETR_CCOMP".format(len(hierarchy)))
     #draw green contours on each of the contours/shapes found
    img = cv2.drawContours(img, contours, -1, (0,255,0), 2)
    cv2.imshow("contours", img)
    cv2.imwrite(OutputImageNew + "\contoursRETR_CCOMP.jpg", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # GetImageProp()
    # TryCropOnFinalSet()
    # DetectChessCorners()
    DetectContours()