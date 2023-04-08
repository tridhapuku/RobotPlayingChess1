import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np

def TakeImageUsingOpenCV():
   

    # select the camera source
    camera_id = 1  # change the value to select the desired camera -- logitech
    cap = cv2.VideoCapture(camera_id)

    # capture an image
    ret, frame = cap.read()

    # save the captured image
    cv2.imwrite("captured_image2.jpg", frame)

    # release the camera
    cap.release()
    return 

def detect_movement(img1, img2):
    # Convert the images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the images
    diff = cv2.absdiff(gray1, gray2)

    # Apply thresholding to the difference image
    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the thresholded image
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    # Get the largest contour (the moved chess piece)
    cnt = max(contours, key=cv2.contourArea)

    # Get the bounding box of the contour
    (x, y, w, h) = cv2.boundingRect(cnt)

    # Get the center of the bounding box
    cx = x + w // 2
    cy = y + h // 2

    # Get the chess square corresponding to the center of the bounding box
    file = chr(ord('a') + (cx - 24) // 64)
    rank = 8 - (cy - 24) // 64

    # Get the movement string
    movement = ''
    for i in range(8):
        for j in range(8):
            if i == rank-1 and j == ord(file)-ord('a'):
                continue
            if gray1[24+i*64,24+j*64] == 0 and gray2[24+i*64,24+j*64] > 0:
                start_file = chr(ord('a') + j)
                start_rank = 8 - i
            elif gray1[24+i*64,24+j*64] > 0 and gray2[24+i*64,24+j*64] == 0:
                end_file = chr(ord('a') + j)
                end_rank = 8 - i
    movement = start_file + str(start_rank) + end_file + str(end_rank)

    # Draw the bounding box and movement string on the original image
    cv2.rectangle(img2, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.putText(img2, movement, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the images
    cv2.imshow('img1', img1)
    cv2.imshow('img2', img2)
    cv2.imshow('diff', diff)

    # Wait for keypress and then close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return movement


def crop_chessboard(img, length):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(type(gray))

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (8,8), None)
    print('ret={} , corners={}'.format(ret,corners))
    if ret == True:
        # Get the corner points of the chessboard
        corner_points = corners.reshape(-1, 2)

        # Get the minimum and maximum x and y coordinates of the corner points
        min_x = min(corner_points[:, 0])
        max_x = max(corner_points[:, 0])
        min_y = min(corner_points[:, 1])
        max_y = max(corner_points[:, 1])

        # Calculate the width and height of the chessboard
        width = max_x - min_x
        height = max_y - min_y

        # Calculate the scaling factor to get the desired length
        scale = length / max(width, height)

        # Scale the chessboard image
        scaled_img = cv2.resize(img, None, fx=scale, fy=scale)

        # Calculate the new width and height of the scaled image
        new_width = int(scale * width)
        new_height = int(scale * height)

        # Calculate the x and y coordinates of the top-left corner of the cropped image
        x = int(min_x * scale)
        y = int(min_y * scale)

        # Crop the scaled image to the desired length
        cropped_img = scaled_img[y:y+new_height, x:x+new_width]

        return cropped_img

    else:
        print("Chessboard not found.")
        return None

import cv2

def find_chessboard_pattern(image_path, min_size=3, max_size=10):
    """
    Finds the chessboard pattern size in an image.

    Args:
        image_path (str): The file path of the image.
        min_size (int): The minimum pattern size to search for.
        max_size (int): The maximum pattern size to search for.

    Returns:
        A tuple representing the pattern size (width, height) if a chessboard pattern is detected, or None if no pattern is found.
    """
    # Load the image
    img = cv2.imread(image_path)

    # Loop through the pattern sizes and find the corners
    for size in range(min_size, max_size + 1):
        print('size={}'.format(size))

        pattern_size = (size, size)
        found, corners = cv2.findChessboardCornersSB(img, pattern_size)

        if found:
            return pattern_size

    # If no pattern is found, return None
    return None

# TakeImageUsingOpenCV()

def ReadAnImageAndFindChessCorners(img1):   
    #Read an image
    # img2 = cv2.imread('5_2.jpg')
    print("Calling function to get pattern")
    # pathImg1 = '5_1.jpg'
 
    img1 =  cv2.imread(pathImg1)
    print(img1.shape)
    # cv2.imshow('image',cropped_img1)
    # cv2.waitKey(0)
    # cv2.imwrite("img1_GrayScale.jpg",cropped_img1)
    # exit()
    print(find_chessboard_pattern(pathImg1, 3))


    # exit()
    print("Calling functn-- to crop image to board_length")
    img1 = crop_chessboard(img1, 500)
    cv2.imwrite("cropped_img1.jpg",img1)

def ResizeImage(img1):
    height,width = img1.shape[:2]
    res = cv2.resize(img1, (int(width/4), int(height/4)), interpolation=cv2.INTER_AREA)
    cv2.imshow('image', res)
    cv2.imwrite("resizedBy4_img1.jpg",res)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

def RotateImage(img):
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    mat = cv2.getRotationMatrix2D(center, 90 ,1)
    rotimg = cv2.warpAffine(img,mat,(h,w))
    cv2.imshow('original',img)
    cv2.imshow('rotated', rotimg)
    cv2.imwrite("rotateBy90_img1.jpg",rotimg)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

def ReturnColorHist(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        hist = cv2.calcHist([img], [i] , None, [256], [0,256])
        plt.plot(hist, color =col)
        plt.xlim([0,256])

    plt.show()

def findAndDrawContours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 30, 200)
    contours , hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
    print("Number of Contours = " ,len(contours))
    cv2.imshow('Canny Edges', canny)
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imshow('Contours',img)
    cv2.imwrite("ContoursOnImg1.jpg", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def TemplateMatching(img, template):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Template',template)
    w,h = template.shape[0], template.shape[1]
    matched = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( matched >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
    cv2.imshow('Matched with Template',img)
    cv2.imwrite('MatchedTemplate.jpg',img)



if __name__ == "__main__":
    pathImg1 = "D:\MS_Related\ASU\CSE598_Robotics\RobotPlayingChess\CameraAndVision\img1.jpg"
    pathResizedImg = "D:\MS_Related\ASU\CSE598_Robotics\RobotPlayingChess\resizedBy4_img1.jpg"
    img_separateWin = "separate_windows1.jpg"

    img1 = cv2.imread(pathImg1)
    img_template = cv2.imread('templates.jpg',0)
    # ResizeImage(img1)
    # RotateImage(img1)
    # ReturnColorHist(img1)
    # findAndDrawContours(cv2.imread(img_separateWin))
    TemplateMatching(cv2.imread('template_matching.jpg',1) , img_template)
