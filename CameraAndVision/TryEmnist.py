import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
import numpy as np
import os

from keras.models import load_model
from keras.models import model_from_json
from matplotlib import pyplot as plt
# %matplotlib inline



absolute_path = os.path.dirname(__file__)
# relative_path = "CameraAndVision\Images"
relative_path = "Images\\new-setup-images"
OutputImageNew = os.path.join(absolute_path, "Images\OutputNew")
full_pathNewSet = os.path.join(absolute_path,relative_path)
full_pathImages = os.path.join(absolute_path, "Images")

#Model Path
ModelPath = os.path.join(absolute_path, "PreTrainedModels")
EMNISTPath = ModelPath + "\\EMNIST-master"

def TryPretrainedModel():
    # Load pre-trained model
    json_file = open(EMNISTPath + '\\model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)


    loaded_model.load_weights(EMNISTPath + '\\model.h5')

    model = loaded_model
    print('Model successfully loaded')
    # model = tf.keras.models.load_model(ModelPath + "\\258epochs_model_7.h5")

    # Load the input image and resize it to 28x28
    # Load the input image with OpenCV and convert it to grayscale
    pathImg = OutputImageNew + "\pawnSmall_2.PNG" 
    img = cv2.imread(pathImg)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize the image to 28x28 and invert the pixel values
    gray = cv2.resize(gray, (28, 28))
    cv2.imshow("grayResize",gray)
    gray = cv2.bitwise_not(gray)
    cv2.imshow("grayBitwiseNot",gray)

    # # Convert the image to a numpy array and normalize the pixel values
    # x = image.img_to_array(gray)
    # x = x / 255.0

    # # Add batch dimension to the input image
    # x = np.expand_dims(x, axis=0)
    # Resize the image to 28x28 and flatten it to a 1D vector
    # img_resized = cv2.resize(gray, (28, 28))
    img_flattened = gray.flatten() / 255.0  # normalize pixel values to between 0 and 1

    # Pass the flattened input image through the model to get the output
    output = model.predict(np.array([img_flattened]))
    

    # Pass the input image through the model to get the output
    # output = model.predict(x)

    # Get the predicted letter
    print(output)
    print(output.shape)
    predicted_letter = chr(np.argmax(output) + 97)  # convert from 0-25 to a-z

    print("The predicted letter is:", predicted_letter)

def TryLoadModel():


    json_file = open(EMNISTPath + '\\model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)


    loaded_model.load_weights(EMNISTPath + '\\model.h5')

    model = loaded_model
    print('Model successfully loaded')

    characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


    #enter input image here
    image = cv2.imread(EMNISTPath + '\\example.png')
    height, width, depth = image.shape

    #resizing the image to find spaces better
    image = cv2.resize(image, dsize=(width*5,height*4), interpolation=cv2.INTER_CUBIC)
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


    #binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)


    #dilation
    kernel = np.ones((5,5), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    #adding GaussianBlur
    gsblur=cv2.GaussianBlur(img_dilation,(5,5),0)


    #find contours
    im2,ctrs, hier = cv2.findContours(gsblur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    m = list()
    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    pchl = list()
    dp = image.copy()
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
        cv2.rectangle(dp,(x-10,y-10),( x + w + 10, y + h + 10 ),(90,0,255),9)
        
    plt.imshow(dp)

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
        # Getting ROI
        roi = image[y-10:y+h+10, x-10:x+w+10]
        roi = cv2.resize(roi, dsize=(28,28), interpolation=cv2.INTER_CUBIC)
        roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        
        roi = np.array(roi)
        t = np.copy(roi)
        t = t / 255.0
        t = 1-t
        t = t.reshape(1,784)
        m.append(roi)
        pred = model.predict_classes(t)
        pchl.append(pred)

    

    pcw = list()
    interp = 'bilinear'
    fig, axs = plt.subplots(nrows=len(sorted_ctrs), sharex=True, figsize=(1,len(sorted_ctrs)))
    for i in range(len(pchl)):
        #print (pchl[i][0])
        pcw.append(characters[pchl[i][0]])
        axs[i].set_title('-------> predicted letter: '+characters[pchl[i][0]], x=2.5,y=0.24)
        axs[i].imshow(m[i], interpolation=interp)
    plt.show()


    predstring = ''.join(pcw)
    print('Predicted String: '+predstring)

if __name__ == "__main__":
    # TryOCR()
    # SliceFromImage()
    TryPretrainedModel()
    # TryLoadModel()
