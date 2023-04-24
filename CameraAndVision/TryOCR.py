import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import pytesseract as pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

absolute_path = os.path.dirname(__file__)
# relative_path = "CameraAndVision\Images"
relative_path = "Images\\new-setup-images"
OutputImageNew = os.path.join(absolute_path, "Images\OutputNew")
full_pathNewSet = os.path.join(absolute_path,relative_path)
full_pathImages = os.path.join(absolute_path, "Images")

def TryOCR():
    # pathImg = OutputImageNew + "\Wikinews_Breaking_News.png" 
    pathImg = OutputImageNew + "\pawnSmall.PNG" 
    img = cv2.imread(pathImg)

    #Try gray , then custom config 
    text = pytesseract.image_to_string(img)
    print(text)


if __name__ == "__main__":
    TryOCR()
