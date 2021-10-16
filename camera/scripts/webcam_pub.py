#!/usr/bin/env python3

import time
import rospy
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def publish_message():
    # Publishing to the video_frames topic
    publisher = rospy.Publisher('video_frames_raw', Image, queue_size=10)
    # This node is call video_publisher
    rospy.init_node('webcam_publisher', anonymous=True)

    # Set required objects
    capture = cv.VideoCapture(0)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    bridge = CvBridge()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        start_time = time.time()
        ret, frame = capture.read()
        if ret == True:
            publisher.publish(bridge.cv2_to_imgmsg(frame))
            rate.sleep()

            end_time = time.time()
            total_time = end_time - start_time
            fps = 1 / total_time
            rospy.loginfo('publishing webcam frame. FPS: %.2f' % fps)


if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass