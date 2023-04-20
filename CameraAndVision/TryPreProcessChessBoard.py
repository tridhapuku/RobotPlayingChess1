import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os

absolute_path = os.path.dirname(__file__)
# relative_path = "CameraAndVision\Images"
relative_path = "Images\captured_imagaes"
full_path = os.path.join(absolute_path,relative_path)
OutputImagePath = os.path.join(absolute_path, "Images\Output")
Crop_hStart , Crop_hEnd = 210 , 420
Crop_wStart , Crop_wEnd = 240 , 450

def DetectChessCorners(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('GrayImg',gray)
    # cv2.imwrite(OutputImagePath + "\Gray1.png", gray)

    ret, corners = cv2.findChessboardCorners(gray,(7,7) , None)
    print("Finding chess board corners done")
    print(corners.shape)

    # return
    if ret == True:
        img = cv2.drawChessboardCorners(img, (7,7) , corners, ret)
        cv2.imshow('Chessboard', img)
        # cv2.waitKey(0)
        cv2.imwrite(OutputImagePath + "\ChessCorners6_8By8.png" , img)
    else:
        print("Chessboard Corners Not found!")

    cv2.destroyAllWindows()

def GetImageProp(img):
    #Get shape & size 
    print(img.shape)
    print(img.size) #total no of pixels
    print(type(img))

def CropImageUsingSlicing(img):
    cropped_img = img[Crop_hStart:Crop_hEnd,Crop_wStart:Crop_wEnd]
    cv2.imshow("cropped" , cropped_img)
    cv2.imwrite(OutputImagePath + "\Cropped11.png", cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def CropAllImagesAndSave(path):
    ImgPrefix = path + "\chessboard_state_"
    ImgPostfix = ".png"
    for i in range(1,13):
        imgName = ImgPrefix + str(i) + ImgPostfix
        img = cv2.imread(imgName) 
        cropped_img = img[Crop_hStart:Crop_hEnd,Crop_wStart:Crop_wEnd]
        cv2.imwrite(OutputImagePath + "\Cropped" + str(i) + ImgPostfix , cropped_img)

if __name__ == "__main__":
    
    # absolute_path = os.path.dirname(__file__)
    # relative_path = "CameraAndVision\Images"
    # full_path = os.path.join(absolute_path,relative_path)

    # pathImg1 = "D:\MS_Related\ASU\CSE598_Robotics\RobotPlayingChess\CameraAndVision\Images\img1.jpg"
    pathResizedImg = "D:\MS_Related\ASU\CSE598_Robotics\RobotPlayingChess\CameraAndVision\Images\captured_imagaes"
    pathImg1 = full_path + "\chessboard_state_11.png"
    pathFolder = "D:\MS_Related\ASU\CSE598_Robotics\RobotPlayingChess\CameraAndVision\Images\captured_imagaes"
    
    Cropped11 = OutputImagePath + "\Cropped6.png"
    CroppedImg11 = cv2.imread(Cropped11)
    # img1 = cv2.imread(pathImg1)
    # GetImageProp(img1)
    # CropImageUsingSlicing(img1)
    # CropAllImagesAndSave(pathFolder)
    DetectChessCorners(CroppedImg11)
    
    # cv2.show()
    # DetectChessCorners(img1)
    # img_template = cv2.imread( path_template,0)
    # ResizeImage(img1)
    # RotateImage(img1)
    # ReturnColorHist(img1)
    # findAndDrawContours(cv2.imread(img_separateWin))
    # TemplateMatching(cv2.imread('.\Images\template_matching.jpg',1) , img_template)
