import os, io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ocr-test-384801-e22a28c4bb36.json'

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
path = 'crop-test1.jpg'
# detect_text("crop-test1.jpg")
from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()

with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
# print(texts)

rectangles = []
for text in texts:
    # vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])
    
    vertices = []
    vertices.append(text.description)
    for index, vertex in enumerate(text.bounding_poly.vertices):
        
        if index in (0,2):
            vertices.append((vertex.x, vertex.y))



    rectangles.append(vertices)

print(rectangles)

# ------------------------------------------------------------
import cv2

# Load image
image = cv2.imread('crop-test1.jpg')

# Define the coordinates of the box
# x, y, w, h = 100, 100, 200, 200
# rectangles = [(1128, 118, 1106, 78), (1215,121,1184,87)]
# x1, y1, x2, y2 = 1128, 118, 1106, 78
# Draw the box

for (desc, left, right) in rectangles:
    cv2.rectangle(image, left, right, (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    letter_x = left[0] + int((right[0]-left[0])/2) - 10
    letter_y = left[1] + int((right[1]-left[1])/2) + 10
    cv2.putText(image, desc, (letter_x, letter_y), font, 3, (0, 0, 255), 2, cv2.LINE_AA)
# cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Show the image
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
