import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import time as time


absolute_path = os.path.dirname(__file__)
# relative_path = "CameraAndVision\Images"
relative_path = "Images\OutputNew\InputImages"
OutputImageNew = os.path.join(absolute_path, "Images\OutputNew")
full_pathNewSet = os.path.join(absolute_path,relative_path)
Crop_hStart , Crop_hEnd = 40 , 970
Crop_wStart , Crop_wEnd = 310 , 1290
OutputCropped = OutputImageNew + "\\Cropped"
InputImagePath = OutputImageNew + "\\InputImages"
# Crop_hStartF , Crop_hEndF = 0, 0
# Crop_wStartF, Crop_wEndF = 0, 0



def ReadImage():
    pathImg = OutputImageNew + "\\a2.jpg" 
    img = cv2.imread(pathImg)
    return img

def GetImageProp():
    # pathImg = full_pathNewSet + "\WIN_20230422_18_46_05_Pro.jpg"

    img = ReadImage()

    print(img.shape)
    #get individual channels and print the values for blue pieces --
    b,g,r = cv2.split(img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    print(hsv.shape)

    #color range to filter out
    lower_range_purple = np.array([200,240,34])
    upper_range_purple = np.array([200,240,82])  # upper range for blue color

    # Create a mask based on the color range
    mask = cv2.inRange(hsv, lower_range_purple, upper_range_purple)
    cv2.imshow("purple_mask", mask)

    # Apply the mask to the original image to filter out the color
    filtered_image = cv2.bitwise_and(img, img, mask=mask)
    # Display the original image and the filtered image side by side
    cv2.imshow('Original Image', img)
    cv2.imshow('Filtered Image', filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






def TryCropOnFinalSet():
    count = 0
    NameImg = "WIN_20230422_17_39_47_Pro.jpg" #"WIN_20230422_18_46_05_Pro.jpg"
    pathImg = InputImagePath + "\\" + NameImg
    img = cv2.imread(pathImg)
    cropped_img = img[Crop_hStart:Crop_hEnd,Crop_wStart:Crop_wEnd]
    cv2.imshow("cropped" , cropped_img)
    cv2.imwrite(OutputCropped + "\Cropped" + str(count) + ".jpg", cropped_img)

    #GetChessCorners and Print corners -- save it by rounding it 
    GetChessCorners(cropped_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def GetChessCorners(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray,(7,7) , None)
    print("Finding chess board corners done")
    if ret == True:
        print(corners.shape)
        
        corners = np.uint16(np.around(corners))
        print(corners)
        # print("---")
        # print(corners[0,0,0])
        # print(corners[0,0,1])
        # print(corners[48,0,1])
        # img = cv2.drawChessboardCorners(img, (7,7) , corners, ret)
        # cv2.imshow('Chessboard', img)
        # # cv2.waitKey(0)
        # cv2.imwrite(OutputCropped + "\ChessCorners0.png" , img)
    else:
        print("Chessboard Corners Not found!")

    # Define the dimensions of the chessboard pattern
    pattern_size = (7, 7)

    #From corners draw blocks --
    corners = corners.reshape(-1, 2)
    # Sort the corner points in row-major order
    corners = corners[np.argsort(corners[:, 1])]
    for i in range(pattern_size[1]):
        corners[i * pattern_size[0]:(i + 1) * pattern_size[0]] = corners[i * pattern_size[0]: (i + 1) * pattern_size[0]][np.argsort(corners[i * pattern_size[0]: (i + 1) * pattern_size[0]][:, 0])]

    # Calculate the x, y coordinates of each block
    for i in range(pattern_size[1] - 1):
        for j in range(pattern_size[0] - 1):
            # Calculate the four corner points of each block
            p1 = corners[i * pattern_size[0] + j]
            p2 = corners[i * pattern_size[0] + j + 1]
            p3 = corners[(i + 1) * pattern_size[0] + j + 1]
            p4 = corners[(i + 1) * pattern_size[0] + j]

            # Calculate the center point of the block
            center_x = int((p1[0] + p2[0] + p3[0] + p4[0]) / 4)
            center_y = int((p1[1] + p2[1] + p3[1] + p4[1]) / 4)

            # Print the x, y coordinates of the center point
            print('Block ({}, {}): ({}, {})'.format(i, j, center_x, center_y))

    for i in range(pattern_size[1] - 1):
        for j in range(pattern_size[0] - 1):
            # Calculate the four corner points of each block
            p1 = corners[i * pattern_size[0] + j]
            p2 = corners[i * pattern_size[0] + j + 1]
            p3 = corners[(i + 1) * pattern_size[0] + j + 1]
            p4 = corners[(i + 1) * pattern_size[0] + j]

            print("Points: {} , {} , {} , {}".format(p1,p2,p3,p4) )
            cv2.line(img,p1,p2,(0,255,0),2) #Blue
            cv2.line(img,p2,p3,(255,0,0),2) #Green
            cv2.line(img,p3,p4,(0,255,0),2) #Red 
            cv2.line(img,p4,p1,(147, 20, 255),2) #Pink   

    cv2.imshow("Drawn_lines",img)
    cv2.imwrite(OutputCropped + "\WithBlocks1.jpg" , img)
    cv2.waitKey()
    #draw lines on img for each block 
    # for 
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
    pathImg = OutputImageNew + "\\a1.jpg"
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
    cv2.imwrite(OutputImageNew + "\contoursA1.jpg", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def DetectCircles():
    pathImg = OutputImageNew + "\\a2.jpg"  #a1.jpg
    img = cv2.imread(pathImg)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray1", gray_img)
    gray_img = cv2.medianBlur(gray_img, 5)
    cv2.imshow("blur", gray_img)
    circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT , 1, 20,
                               param1=100, param2=70,minRadius=0,maxRadius=0)
    print(circles.shape)
    print(circles)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(img, (i[0],i[1]), i[2], (0,255,0) , 2)
        
    cv2.imwrite(OutputImageNew + "\\a2Lines1.jpg", img)
    cv2.imshow("Circles", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def CaptureImage(Number):
    #Capture image & save image as imageNumber
    print()

def Take2ImagesAndDivideInto64Blocks():
    print()

ListOfChars = ['p', 'q', 'r', 'n', 'b','k','P', 'Q','R','N', 'B','K','/', '*']

def StringToFen(str1):
    # loop for entire length
    result_fen = ""
    count = 0
    for i in range(len(str1)):
        #if * , count till * or \ 
        if str1[i] in ListOfChars:
            if str1[i] == "*":
                count = count + 1
            else:
                if str1[i - 1] == "*":
                    result_fen = result_fen + str(count) + str1[i]
                    count = 0
                else:
                    result_fen = result_fen + str1[i]
        else:
            print("Check output from ocr -- Unknown Characters {}".format(str1[i]))

    print("result_fen = {}".format(result_fen))


def TestStringToFen():
    str1 = "rnbqkbnr/pp*ppppp/********/**p*****/****P***/********/PPPP*PPP/RNBQKBNR"
    print(StringToFen(str1))
        
RowNos = [1,2,3,4,5,6,7,8]
ColNos = ["a" , "b" , "c", "d", "e","f", "g","h"]
RowNosAsStr = str(RowNos)

listOfTuples = [('a1', 'R'), ('a2', 'P'), ('a3', '*'), ('a4', '*'), ('a5', '*'), ('a6', '*'), ('a7', 'p'), ('a8', 'r'), ('b1', 'N'), ('b2', 'P'), ('b3', '*'), ('b4', '*'), ('b5', '*'), ('b6', '*'), ('b7', 'p'), ('b8', 'n'), ('c1', 'B'), ('c2', 'P'), ('c3', '*'), ('c4', '*'), ('c5', '*'), ('c6', '*'), ('c7', 'p'), ('c8', 'b'), ('d1', 'K'), ('d2', 'P'), ('d3', '*'), ('d4', '*'), ('d5', 'P'), ('d6', '*'), ('d7', '*'), ('d8', 'k'), ('e1', 'Q'), ('e2', '*'), ('e3', '*'), ('e4', '*'), ('e5', '*'), ('e6', '*'), ('e7', 'p'), ('e8', 'q'), ('f1', 'B'), ('f2', 'P'), ('f3', '*'), ('f4', '*'), ('f5', '*'), ('f6', 'n'), ('f7', 'p'), ('f8', 'b'), ('g1', 'N'), ('g2', 'P'), ('g3', '*'), ('g4', '*'), ('g5', '*'), ('g6', '*'), ('g7', 'p'), ('g8', '*'), ('h1', 'R'), ('h2', '*'), ('h3', '*'), ('h4', 'P'), ('h5', '*'), ('h6', '*'), ('h7', 'p'), ('h8', 'r')]

def FindStrMovement(str1, str2):

    #Loop through each of the 64 nos -- 
    count = 0
    result_move = ""
    for i in RowNos:
        for j in ColNos:
            #if str1 is full & str2 empty this is location of piece moved
            # if str1 is empty & str2 full this is location of dest 
            if str1[i] == "*" :
                print() 


def CheckListOfTuples():

    # for tuple in listOfTuples:
    #     print(tuple[0] + "\\" + tuple[1] )

    for i in range(len(listOfTuples)):
        print(listOfTuples[i][0] + "\\" + listOfTuples[i][1])
        # print(listOfTuples[i][1])

ListOfPieces = ['p', 'q', 'r', 'n', 'b','k','P', 'Q','R','N', 'B','K']

def ReturnTuple():
    return listOfTuples

def GetUciMove(listOfTuples1, listOfTuples2):
    result_uci = ""
    countOfPiecesMoved = 0
    listOfPiecesMoved = []
    prev_uci , next_uci = "" , ""
    piece_moved = ""

    print("Testing sleep - 3secs")
    time.sleep(3)
    #loop through each item
    for i  in range(len(listOfTuples1)):
        #if firstloc is full & secondloc is empty --> this piece moved -- prev_uci 
        #if firstloc is empty & secondloc is full --> this piece destinatio -- next_uci
        pieceInFirstBoard = listOfTuples1[i][1]
        pieceIn2ndBoard = listOfTuples2[i][1]

        if (pieceInFirstBoard in ListOfPieces) and pieceIn2ndBoard == "*":
            listOfPiecesMoved.append(pieceInFirstBoard)
            countOfPiecesMoved = countOfPiecesMoved + 1
            prev_uci = listOfTuples1[i][0]
            piece_moved = listOfTuples1[i][1]
            # break
        else:
            continue

    #iterate through all locations in p2 & get its next location
    for i  in range(len(listOfTuples2)):
        if piece_moved == listOfTuples2[i][1]:
            next_uci = listOfTuples2[i][0]


    if countOfPiecesMoved > 1:
        print("From Past Move to Present Move --multiple moves detected")
        print(listOfPiecesMoved)
    else:
        result_uci = prev_uci + next_uci

    return result_uci

def TestGetUciMove():
    listOfTuples1 = [('a1', 'R'), ('a2', 'P'), ('a3', '*'), ('a4', '*'), ('a5', '*'), ('a6', '*'), ('a7', 'p'), ('a8', 'r'), ('b1', 'N'), ('b2', 'P'), ('b3', '*'), ('b4', '*'), ('b5', '*'), ('b6', '*'), ('b7', 'p'), ('b8', 'n'), ('c1', 'B'), ('c2', 'P'), ('c3', '*'), ('c4', '*'), ('c5', '*'), ('c6', '*'), ('c7', 'p'), ('c8', 'b'), ('d1', 'K'), ('d2', 'P'), ('d3', '*'), ('d4', '*'), ('d5', 'P'), ('d6', '*'), ('d7', '*'), ('d8', 'k'), ('e1', 'Q'), ('e2', '*'), ('e3', '*'), ('e4', '*'), ('e5', '*'), ('e6', '*'), ('e7', 'p'), ('e8', 'q'), ('f1', 'B'), ('f2', 'P'), ('f3', '*'), ('f4', '*'), ('f5', '*'), ('f6', 'n'), ('f7', 'p'), ('f8', 'b'), ('g1', 'N'), ('g2', 'P'), ('g3', '*'), ('g4', '*'), ('g5', '*'), ('g6', '*'), ('g7', 'p'), ('g8', '*'), ('h1', 'R'), ('h2', '*'), ('h3', '*'), ('h4', 'P'), ('h5', '*'), ('h6', '*'), ('h7', 'p'), ('h8', 'r')]

    listOfTuples2 = [('a1', 'R'), ('a2', 'P'), ('a3', 'P'), ('a4', '*'), ('a5', '*'), ('a6', '*'), ('a7', 'p'), ('a8', 'r'), ('b1', 'N'), ('b2', '*'), ('b3', '*'), ('b4', '*'), ('b5', '*'), ('b6', '*'), ('b7', 'p'), ('b8', 'n'), ('c1', 'B'), ('c2', 'P'), ('c3', '*'), ('c4', '*'), ('c5', '*'), ('c6', '*'), ('c7', 'p'), ('c8', 'b'), ('d1', 'K'), ('d2', 'P'), ('d3', '*'), ('d4', '*'), ('d5', 'P'), ('d6', '*'), ('d7', '*'), ('d8', 'k'), ('e1', 'Q'), ('e2', '*'), ('e3', '*'), ('e4', '*'), ('e5', '*'), ('e6', '*'), ('e7', 'p'), ('e8', 'q'), ('f1', 'B'), ('f2', 'P'), ('f3', '*'), ('f4', '*'), ('f5', '*'), ('f6', 'n'), ('f7', 'p'), ('f8', 'b'), ('g1', 'N'), ('g2', 'P'), ('g3', '*'), ('g4', '*'), ('g5', '*'), ('g6', '*'), ('g7', 'p'), ('g8', '*'), ('h1', 'R'), ('h2', '*'), ('h3', '*'), ('h4', 'P'), ('h5', '*'), ('h6', '*'), ('h7', 'p'), ('h8', 'r')]

    print(GetUciMove(listOfTuples1, listOfTuples2))

if __name__ == "__main__":
    # GetImageProp()
    # TryCropOnFinalSet()
    # DetectChessCorners()
    # DetectContours()
    # DetectCircles()
    # TestStringToFen()
    # CheckListOfTuples()
    TestGetUciMove()
