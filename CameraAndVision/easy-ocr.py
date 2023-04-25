import easyocr

reader = easyocr.Reader(['en'])

image = 'test.jpg'

results = reader.readtext(image)
