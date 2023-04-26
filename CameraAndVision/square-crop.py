import cv2
import numpy as np

def crop_image(filename):
    
    # Load image
    img = cv2.imread(filename)
    # crop to chessboard
    img_crop = img[14:960, 357:1300]
    
    return img_crop

#reference image
img_crop = crop_image("CameraAndVision\data\\testing_images\crop-test9.jpg")

#create this folder beforehand         
test_path = "CameraAndVision\\data\\split_images\\" 

# Convert to grayscale
gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
pattern_size = (7, 7)


ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

img_crop2 = img_crop.copy()

# Find the chessboard corners
found, corners = cv2.findChessboardCorners(thresh, pattern_size, cv2.CALIB_CB_FAST_CHECK)
# cv2.imshow("cropped", img_crop)
# cv2.imshow("thresh", thresh)
# print(corners)
# print(type(corners))
# corners = np.uint16(np.around(corners))
# print((corners))



if not found:
    print('Chessboard corners not found')

else:
    # Draw the corners on the input image
    cv2.drawChessboardCorners(img_crop2, pattern_size, corners, found)

    # Display the input image with the corners detected
    # cv2.imshow('Chessboard Corners', img_crop2)
    
cv2.waitKey(0)
cv2.destroyAllWindows()


    #a1
a8 = img_crop2.copy()
hh, ww = 106, 106
start_index_array = [0,7,14,21,28,35,42]
for j in range(8,0,-1):
    col = 97
    if j > 1:   # for rows 1-7
        print("rows 1-7")
        start_index = start_index_array[8-j]

        for i in range(0,8):
            if i <7: # for columns a-g
                corner_x, corner_y = int(corners[start_index+i][0][0]), int(corners[start_index+i][0][1])
                square_crop = a8[corner_y:corner_y+hh, corner_x:corner_x+ww] #a8
                cv2.imwrite(chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            else: # for column h

                corner_x, corner_y = int(corners[start_index+i-1][0][0]), int(corners[start_index+i-1][0][1])
                square_crop = a8[corner_y:corner_y+hh, corner_x-ww:corner_x] #a1
                cv2.imwrite(chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            col+=1
            
    else:     # for 8th row
        start_index = start_index_array[8-j-1]
        
        for i in range(0,8):
            if i <7:
                corner_x, corner_y = int(corners[start_index+i][0][0]), int(corners[start_index+i][0][1])
                square_crop = a8[corner_y-hh:corner_y, corner_x:corner_x+ww] #a8
                cv2.imwrite(chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            else:

                corner_x, corner_y = int(corners[start_index+i-1][0][0]), int(corners[start_index+i-1][0][1])
                square_crop = a8[corner_y-hh:corner_y, corner_x-ww:corner_x] #a1
                cv2.imwrite(chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            col+=1
            
          
            
# testing for random image using hardcoded coordinates

test_image = crop_image("CameraAndVision\data\\testing_images\move0.jpg")

start_index_array = [0,7,14,21,28,35,42]
for j in range(8,0,-1):
    col = 97
    if j > 1:   # for rows 1-7
        start_index = start_index_array[8-j]

        for i in range(0,8):
            if i <7:
                corner_x, corner_y = int(corners[start_index+i][0][0]), int(corners[start_index+i][0][1])
                square_crop = test_image[corner_y:corner_y+hh, corner_x:corner_x+ww] #a8
                cv2.imwrite(test_path+chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            else:

                corner_x, corner_y = int(corners[start_index+i-1][0][0]), int(corners[start_index+i-1][0][1])
                square_crop = test_image[corner_y:corner_y+hh, corner_x-ww:corner_x] #a1
                cv2.imwrite(test_path+chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            col+=1
            
    else:     # for 8th row
        start_index = start_index_array[8-j-1]
        
        for i in range(0,8):
            if i <7:
                corner_x, corner_y = int(corners[start_index+i][0][0]), int(corners[start_index+i][0][1])
                square_crop = test_image[corner_y-hh:corner_y, corner_x:corner_x+ww] #a8
                cv2.imwrite(test_path+chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            else:

                corner_x, corner_y = int(corners[start_index+i-1][0][0]), int(corners[start_index+i-1][0][1])
                square_crop = test_image[corner_y-hh:corner_y, corner_x-ww:corner_x] #a1
                cv2.imwrite(test_path+chr(col)+str(j)+".jpg", square_crop)
                print("saving", chr(col)+str(j)+".jpg")
            col+=1
