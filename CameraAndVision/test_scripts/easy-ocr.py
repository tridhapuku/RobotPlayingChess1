import easyocr

reader = easyocr.Reader(['en'])

image = 'CameraAndVision\crop-test1-row1.jpg'

results = reader.readtext(image)
print(results)
