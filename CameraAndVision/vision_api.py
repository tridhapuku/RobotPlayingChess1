import os, io
from google.cloud import vision
import cv2 as cv2
import glob
import numpy as np

def crop_image(filename):
        
        # Load image
        img = cv2.imread(filename)

        # crop to chessboard
        # img_crop = gray[119:771, 556:1203]
        img_crop = img[14:960, 357:1300]
        
        return img_crop

def detect_text(path, client):
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    # response = client.text_detection(image=image, image_context={"language_hints": ["en"]})
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def draw_rectangle(path, detected_image_path):
    image2 = cv2.imread(path)

    for (desc, left, right) in rectangles:
        cv2.rectangle(image2, left, right, (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        letter_x = left[0] + int((right[0]-left[0])/2) - 10
        letter_y = left[1] + int((right[1]-left[1])/2) + 10
        cv2.putText(image2, desc, (letter_x, letter_y), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    # Show the image
    cv2.imwrite(detected_image_path, image2)
    # cv2.imshow('image2', image2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def get_detected_tuples():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'CameraAndVision\\ocr-test-384801-e22a28c4bb36.json'
    detected_image_path = "CameraAndVision\data\detected\detected.jpg"

    detect_dict = {"ROOK": "R",
                "rook": "r",
                "PAWN": "P",
                "pawn": "p",
                "umed": "p",
                "uned": "p",
                "NTX": "N",
                "ntx": "n",
                "tx": "n",
                "DISH": "B",
                "BISH": "B",
                "HS10": "B",
                "bish": "b",
                "KING": "K",
                "ONIX": "K",
                "king": "k",
                "QUEE": "Q",
                "quee": "q",
                "aanb": "q",
                }


    # crop_image() only works for new setup images to crop to chessboard
    
    # new_path = 'CameraAndVision\move5.jpg'

    client = vision.ImageAnnotatorClient()

    # texts_list = detect_text(new_path)


    # rectangles = []
    # for text in texts_list:
    #     # vertices = (['({},{})'.format(vertex.x, vertex.y)
    #     #                 for vertex in text.bounding_poly.vertices])
        
    #     vertices = []
    #     vertices.append(text.description)
    #     for index, vertex in enumerate(text.bounding_poly.vertices):
            
    #         if index in (0,2):
    #             vertices.append((vertex.x, vertex.y))



    #     rectangles.append(vertices)
    # print(len(rectangles))
    # print(rectangles)

    # draw_rectangle(new_path, detected_image_path)

    # ------------------------------------------------------------

    print("Starting detection...")

    split_images_path = 'CameraAndVision\data\split_images'
    file_list = glob.glob(split_images_path+'\*')
    print(file_list[0], len(file_list))
    print(file_list[0].split('\\')[3])

    detected_tuple = []
    for f in file_list:
        position = f.split('\\')[3]
        texts_list = detect_text(f, client)
        if not texts_list:
            piece = '*'
        else:
            if texts_list[-1].description in detect_dict:
                piece = detect_dict[texts_list[-1].description]
            else: 
                piece = texts_list[-1].description

        detected_tuple.append((position[:2], piece))

    # for i in detected_tuple:
    #     print(i)

    # print(detected_tuple)
    return detected_tuple


def TakeImageUsingOpenCV(count):
   
    print("Taking image from camera...")
    # select the camera source
    camera_id = 1  # change the value to select the desired camera -- logitech
    cap = cv2.VideoCapture(camera_id)

    # capture an image
    ret, frame = cap.read()

    # save the captured image
    cv2.imwrite("CameraAndVision\data\captured_live_images" + "\captured_image"+str(count)+".jpg", frame)
    
    # release the camera
    cap.release()
    print("Saved image")
    return 

corners = np.array([[[782, 814]],
 [[672, 815]],
 [[565, 811]],
 [[460, 809]],
 [[351, 810]],
 [[244, 808]],
 [[137, 810]],
 [[785, 705]],
 [[674, 708]],
 [[567, 704]],
 [[457, 701]],
 [[352, 702]],
 [[244, 702]],
 [[133, 703]],
 [[782, 597]],
 [[673, 600]],
 [[566, 595]],
 [[461, 594]],
 [[352, 595]],
 [[242, 595]],
 [[137, 596]],
 [[786, 489]],
 [[673, 488]],
 [[566, 488]],
 [[460, 488]],
 [[351, 487]],
 [[245, 487]],
 [[135, 487]],
 [[782, 378]],
 [[673, 382]],
 [[567, 378]],
 [[461, 376]],
 [[352, 378]],
 [[242, 377]],
 [[136, 378]],
 [[787, 270]],
 [[676, 272]],
 [[567, 271]],
 [[460, 270]],
 [[350, 271]],
 [[243, 268]],
 [[133, 271]],
 [[784, 163]],
 [[674, 165]],
 [[565, 161]],
 [[458, 163]],
 [[353, 163]],
 [[242, 162]],
 [[137, 163]]])

def SplitImage(image_path):
    hh, ww = 106, 106
    test_image = crop_image(image_path)
    test_path = "CameraAndVision\\data\\split_images\\" 
    print("Splitting image to individual boxes...")
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

def PreProcessImage(count):
    # full_setup_image = CaptureImage()
    # full_setup_image = "CameraAndVision\data\\testing_images\move5.jpg"
    TakeImageUsingOpenCV(count)
    full_setup_image = "CameraAndVision\data\captured_live_images" + "\captured_image"+str(count)+".jpg"
    SplitImage(full_setup_image)
    return_tuple = get_detected_tuples()
    return return_tuple

if __name__ == "__main__":
    # SplitImage("CameraAndVision\data\captured_live_images\captured_image0.jpg")
    SplitImage("CameraAndVision\data\\testing_images\move0.jpg")
    return_tuple = get_detected_tuples()
    print(return_tuple)