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
OCRTrialPath = OutputImageNew + "\\ForOCRTrial"

NameOfImg = "CompletePic.JPG"
def ReadImage():
    # pathImg = OutputImageNew + "\pawnSmall_2.PNG" 
    pathImg = OCRTrialPath + "\\" + NameOfImg
    img = cv2.imread(pathImg)
    return img



def FilterUsingColor():
    img = ReadImage()

    # Convert image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    

def TryOCR():
    # pathImg = OutputImageNew + "\Wikinews_Breaking_News.png" 
    # pathImg = OutputImageNew + "\pawnSmall_2.PNG" 
    # img = cv2.imread(pathImg)
    img = ReadImage()

    #Try gray , then custom config 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    thresh = cv2.threshold(gray, 127, 255, 0)[1]
    cv2.imshow("gray1",thresh)
    cv2.imwrite(OCRTrialPath + "\gray_" + NameOfImg, thresh)
    text = pytesseract.image_to_string(thresh)
    print(text)

def TryOCRWithCustomConfig():
    # pathImg = OutputImageNew + "\Wikinews_Breaking_News.png" 
    pathImg = OutputImageNew + "\\PieceNames.PNG" 
    img = cv2.imread(pathImg)

    # Set the list of allowed letters
    letters = ['p', 'r', 'n', 'b', 'k', 'q', 'P', 'R', 'N', 'B', 'K', 'Q']
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray1", gray)


    # Set the configuration parameters for Tesseract OCR
    config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=' + ''.join(letters)

    # Perform OCR on the image
    text = pytesseract.image_to_string(gray, config=config)

    # Check if the detected text is a valid letter
    if len(text) >= 1 and text in letters:
        print('Detected letter:', text)
    else:
        print('Letter not detected.')


def SliceFromImage():
    pathImg = OutputImageNew + "\pawnSmall_2.PNG" 
    img = cv2.imread(pathImg)
    print(img.shape)
    b,g,r = cv2.split(img)
    print(b.shape)
    print(b)

    # cropped_img = img[Crop_hStart:Crop_hEnd,Crop_wStart:Crop_wEnd]

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 


def TryOCRWithCustomConfigNanoNets():
    img = ReadImage()



if __name__ == "__main__":
    TryOCR()
    # SliceFromImage()
    # TryOCRWithCustomConfig()
