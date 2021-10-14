#!/usr/bin/env python3

import rospy
import cv2 as cv
import socket, imagezmq
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


# Get local hostname and define imagezmq object & client IP address for video stream
host = socket.gethostname()
sender = imagezmq.ImageSender(connect_to="tcp://192.168.1.30:5555")


def callback(data):
    bridge = CvBridge()
    rospy.loginfo('receiving & streaming processed webcam frame')
    current_frame = bridge.imgmsg_to_cv2(data)    
    try:
        sender.send_image(host, current_frame)
    except:
        pass

    # # Local webcam display
    # cv.namedWindow("RPi Webcam", 0)
    # cv.resizeWindow("RPi Webcam", 1280, 720)
    # cv.imshow("RPi Webcam", current_frame)
    # cv.waitKey(1)


def receive_message():
    rospy.init_node('webcam_viewer', anonymous=True)
    rospy.Subscriber('video_frames_processed', Image, callback)
    rospy.spin()
    cv.destroyAllWindows()


if __name__ == '__main__':
    receive_message()