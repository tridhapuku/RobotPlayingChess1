#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os

image_saved = False

def image_callback(msg):
    # Exit if image already saved
    global image_saved
    if image_saved:
        return

    rospy.loginfo("Received image message with %dx%d resolution and encoding %s", msg.width, msg.height, msg.encoding)
    # Convert the received ROS Image message to OpenCV format
    try:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    except CvBridgeError as e:
        print("Failed to convert image: %s" % str(e))
        return
    
    # Define the output folder and filename
    output_folder = "/home/catkin_ws/captured_images"
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    #     os.chmod(output_folder, 0o777)
    filename = "chessboard_state_day_.png"
    # output_path = os.path.join(output_folder, filename)
    output_path = filename

    # Save the image as a JPEG file
    try:
        cv2.imwrite(output_path, cv_image)
        rospy.loginfo("Image saved to %s" % output_path)
        image_saved = True
    except Exception as e:
        rospy.logerr("Failed to save image to %s: %s" % (output_path, str(e)))
        return
        

    

def listener():
    rospy.init_node('image_listener', anonymous=True)
    rospy.Subscriber("/camera/color/image_raw", Image, image_callback)
    rospy.spin()
      

if __name__ == '__main__':
    listener()