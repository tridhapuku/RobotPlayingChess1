#!/usr/bin/env python3

import numpy as np
import rospy
from sensor_msgs.msg import Image, JointState
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import sys

state_read = False
positions = []

def state_callback(msg):
    global state_read
    global positions

     # Read joint positions
    if state_read:
        return
    try:
        positions = np.array([msg.position[0], msg.position[1], msg.position[2], msg.position[3], msg.position[4], 0])
        state_read = True
    except Exception as e:
        rospy.logerr("Failed to read joint states: %s" % str(e))
    rospy.loginfo("\nReceived join positions: %s" % str(positions))


    
def listener():
    rospy.init_node('joint_listener', anonymous=True)
    rospy.Subscriber("/cube_stack_arm/joint_states", JointState , state_callback)
    rospy.spin()

# Convert joint positions and save     
def save_joint_states():
    position_rad_input = positions
    position_command = [0, 0, 0, 0, 0]
    # Flip signs
    try:
        position_rad = [(-1 * float(x)) for x in position_rad_input]
    except ValueError:
        rospy.logerr("Invalid list argument")
        sys.exit(1)

    for i in range(len(position_rad) - 1):
        position_command[i] = int(round((1023/300) * (150 - (180*7/22)*position_rad[i]), 0))

    with open("/home/hiteshbhadana/catkin_ws/converted_commands.txt", 'a') as f:
        position_command_str = ": [" + (",").join(str(number) for number in position_command) + "]\n"
        print("\n")
        rospy.loginfo("\nConverted joint positions: %s" % position_command_str)
        save = input("Do you want to save the positions (yes/no): ")
        if save == 'yes' or save == 'Yes' or save == 'True' or save == 'true':
            state = input("Enter the name for positions: ")
            try:
                f.write('"' + state + '"' + position_command_str)
                print("\n")
                rospy.loginfo("\nPositions saved successfully: %s" % (state + position_command_str))
            except ValueError as e:
                rospy.logerr("Error saving: %s" % str(e))

      

if __name__ == '__main__':
    listener()
    save_joint_states()