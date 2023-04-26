import cv2

reference_image = "CameraAndVision\crop-test9.jpg"

def crop_image(filename):
    
    # Load image
    img = cv2.imread(filename)
    # crop to chessboard
    img_crop = img[14:960, 357:1300]
    
    return img_crop

def initialize_board():
    #reference image
    img_crop = crop_image(reference_image)

    # Convert to grayscale
    gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
    pattern_size = (7, 7)


    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    
    # Find the chessboard corners
    found, corners = cv2.findChessboardCorners(thresh, pattern_size, cv2.CALIB_CB_FAST_CHECK)

    # print images for debug
    # img_crop2 = img_crop.copy()
    # cv2.imshow("cropped", img_crop)
    # cv2.imshow("thresh", thresh)
    # # cv2.imshow("resized", resized_img)

    if not found:
        print('Chessboard corners not found.')
        return

    else:
        print("Chessboard corners found!\n Saving the coordinates...")

        return corners
        # Draw the corners on the input image
        # cv2.drawChessboardCorners(img_crop2, pattern_size, corners, found)

        # Display the input image with the corners detected
        # cv2.imshow('Chessboard Corners', img_crop2)
        
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()