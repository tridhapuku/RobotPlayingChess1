

def TakeImageUsingOpenCV():
    import cv2

    # select the camera source
    camera_id = 1  # change the value to select the desired camera -- logitech
    cap = cv2.VideoCapture(camera_id)

    # capture an image
    ret, frame = cap.read()

    # save the captured image
    cv2.imwrite("captured_image2.jpg", frame)

    # release the camera
    cap.release()
    return 


TakeImageUsingOpenCV()
