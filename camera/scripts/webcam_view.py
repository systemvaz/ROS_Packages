#!/usr/bin/env python3

import time
import rospy
import cv2 as cv
import socket, imagezmq
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


# Get local hostname and define imagezmq object & client IP address for video stream
host = socket.gethostname()
sender = imagezmq.ImageSender(connect_to="tcp://192.168.1.30:5555")

fps = 0

def callback(data):
    start_time = time.time()
    bridge = CvBridge()
    current_frame = bridge.imgmsg_to_cv2(data)
    current_frame = cv.resize(current_frame, (640, 360))
    sender.send_image(host, current_frame)
    end_time = time.time()
    total_time = end_time - start_time
    fps = 1 / total_time
    rospy.loginfo('receiving & streaming. FPS: %.2f' % fps)
    

def receive_message():
    rospy.init_node('webcam_viewer', anonymous=True)
    rospy.Subscriber('video_frames_processed', Image, callback)
    rospy.spin()
    cv.destroyAllWindows()


if __name__ == '__main__':
    try:
        receive_message()
    except rospy.ROSInterruptException:
        pass