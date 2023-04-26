import os, io
from google.cloud import vision
import cv2
import glob

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
def crop_image(filename):
    
    # Load image
    img = cv2.imread(filename)

    # crop to chessboard
    # img_crop = gray[119:771, 556:1203]
    img_crop = img[14:960, 357:1300]
    
    return img_crop

def detect_text(path):
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    # response = client.text_detection(image=image, image_context={"language_hints": ["en"]})
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def draw_rectangle(path):
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

new_path = 'CameraAndVision\move5.jpg'

client = vision.ImageAnnotatorClient()

texts_list = detect_text(new_path)


rectangles = []
for text in texts_list:
    # vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])
    
    vertices = []
    vertices.append(text.description)
    for index, vertex in enumerate(text.bounding_poly.vertices):
        
        if index in (0,2):
            vertices.append((vertex.x, vertex.y))



    rectangles.append(vertices)
print(len(rectangles))
print(rectangles)

draw_rectangle(new_path)

# ------------------------------------------------------------


split_images_path = 'CameraAndVision\data\split_images'
file_list = glob.glob(split_images_path+'\*')
print(file_list[0], len(file_list))
print(file_list[0].split('\\')[2])

detected = []
for f in file_list:
    position = f.split('\\')[2]
    texts_list = detect_text(f)
    if not texts_list:
        piece = '*'
    else:
        if texts_list[-1].description in detect_dict:
            piece = detect_dict[texts_list[-1].description]
        else: 
            piece = texts_list[-1].description

    detected.append((position[:2], piece))

# for i in detected:
#     print(i)

print(detected)

