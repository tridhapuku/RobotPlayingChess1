#!/usr/bin/env python3

import numpy as np
import rospy
from sensor_msgs.msg import Image, JointState
from cube_stack_env.msg import SyncSetPositions
from std_msgs.msg import Float64MultiArray
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import sys
from scipy.interpolate import CubicSpline


# Function to convert joint positions into angle in radians for Gazebo
def convert_position2rad(position):
    converted_position = [0, 0, 0, 0, 0]
    for i in range(len(position)):
        converted_position[i] = (150 - 300 * position[i] /1023) * 22 / (180 * 7)
        if i == 4:
            converted_position[i] = -0.1

    # Flinp signs due to URDF config problem
    position_rad_converted = [(-1 * x) for x in converted_position]

    return position_rad_converted

# Function for path planning to make the move
def get_motion_path(move="d8d6", environment="real"):
    # Dicitionary with all positions
    mapping = {"sitting": [511,119,980,755,511],
            "pick_rest": [511,548,833,636,513],
            "d8_pick": [464,575,933,659,512],
            "d8_picked": [464,553,905,659,514],
            "d6_place": [482,632,811,679,514]
            }

    # Get key from chess enginer suggested move
    initial_position_key = move[:2] + "_pick"
    final_position_key = move[-2:] + "_place"

    # Implement grip and release
    grip = mapping[initial_position_key][0:4]
    grip.append(290)
    release = mapping[final_position_key][0:4]
    release.append(411)
    mapping["grip"] = grip
    mapping["release"] = release

    # Steps to follow to make a single move
    motion_path_str = "sitting " + "pick_rest " + initial_position_key + " grip " + "pick_rest " + final_position_key + " release " + "pick_rest " + "sitting" 
    motion_path = []

    # Get a list of joint angles for path to be followed
    if environment == "gazebo":
        for position in motion_path_str.split():
            motion_path.append(convert_position2rad(mapping[position]))
    elif environment == "real":
        flag = 1
        for position in motion_path_str.split():
            if position == "grip" or position == "release":
                flag *= -1
            if flag == 1:
                current_position = mapping[position][0:4]
                current_position.append(411)
                motion_path.append(current_position)
            if flag == -1:
                current_position = mapping[position][0:4]
                current_position.append(225)
                motion_path.append(current_position)
    else:
        exit("ERROR!! wrong environment: {}".format(environment))

    return motion_path

# Function to fit a cubic spline
def discretize_trajectory(motion_path, steps=10):
    new_motion_path = []
    for i in range(len(motion_path)-1):
        number_of_steps = steps
        if i == 0 or i == 7:
            number_of_steps = steps * 4
        elif i == 2 or i == 5:
            number_of_steps = steps * 0
        start_point = np.array(motion_path[i])
        end_point = np.array(motion_path[i+1])
        diff = end_point - start_point
        step_size = diff / (number_of_steps + 1)  # number_of_steps + 1 instead of number_of_steps to also include the endpoint
        for j in range(0, number_of_steps + 1):
            new_motion_path.append(list(start_point + j*step_size))
        new_motion_path.append(list(end_point))

    # Add the last point (it's not included in the loop)
    new_motion_path.append(list(np.array(motion_path[-1])))

    return new_motion_path


# Publisher for gazebo
def joint_angle_publisher_gazebo(motion_path, given_rate=0.1):
    pub = rospy.Publisher('/cube_stack_arm/arm_position_controller/command',Float64MultiArray, queue_size=10)
    rospy.init_node('state_publisher_gazebo', anonymous=True)
    rate = rospy.Rate(given_rate)
    rospy.loginfo("Publishing joint angles...")

    i = 0
    while not rospy.is_shutdown() and i < len(motion_path):
        msg = Float64MultiArray()
        msg.data = motion_path[i] # publish sequence of joint angles
        pub.publish(msg)
        rospy.loginfo("Published joint angles: {}". format(msg.data))
        i += 1
        rate.sleep()

# Publisher for actual hardware
def joint_angle_publisher_hardware(motion_path, given_rate=0.1):
    pub = rospy.Publisher('/cube_stack_arm/sync_set_positions', SyncSetPositions, queue_size=10)
    rospy.init_node('state_publisher_hardware', anonymous=True)
    rate = rospy.Rate(given_rate)
    rospy.loginfo("Publishing joint angles...")

    i = 0
    last = 411
    while not rospy.is_shutdown() and i < len(motion_path):
        msg = SyncSetPositions()
        msg.position = [int(x) for x in motion_path[i]]
        msg.id = [1,2,3,4,5]
        pub.publish(msg)
        rospy.loginfo("Published joint angles: {}". format(msg))
        rate.sleep()
        current = int(motion_path[i][4])
        if last != current:
            rate = rospy.Rate(0.5)
        else:
            rate = rospy.Rate(given_rate)
        last = current
        i += 1


if __name__ == '__main__':
    move = "d8d6"
    environment = "real"
    given_rate = 15
    number_of_steps = 100
    to_discretize = True

    # Ensure correct environment and rate are selected
    print("Selected environment: {}\t Give rate: {}\t Number of steps: {}, To discretize?: {}".format(environment, given_rate, number_of_steps, to_discretize))
    answer = input("Do you want to continue? (y/n): ")
    if answer != "y":
        exit("Exiting")
    answer = input("Is the robot in home position? (y/n): ")
    if answer != 'y':
        exit("Please set the robot to home position and then run")

    motion_path = get_motion_path(move, environment)
    # # Print planned motion
    # for motion in motion_path:
    #     print(motion)
    # input()


    if to_discretize == True:
        motion_path = discretize_trajectory(motion_path, number_of_steps)
    # Print discretized motion path
    # for i in range(15):
    #     print(motion_path[i][:])
    # input()

    # Publish joint states
    try:
        if environment == "gazebo":
            joint_angle_publisher_gazebo(motion_path, given_rate)
        elif environment == "real":
            # joint_angle_publisher_hardware([[511,511,511,511,411]], 0.1)
            # joint_angle_publisher_hardware([[511,119,980,755,411]], 0.1)
            joint_angle_publisher_hardware(motion_path, given_rate)
        else:
            exit("ERROR!! wrong environment: {}".format(environment))
    except rospy.ROSInterruptException as e:
        print("STOPPED: %s" % e)

    