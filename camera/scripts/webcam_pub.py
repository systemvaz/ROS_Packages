#!/usr/bin/env python3

import rospy
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def publish_message():
    # Publishing to the video_frames topic
    publisher = rospy.Publisher('video_frames_raw', Image, queue_size=30)
    # This node is call video_publisher
    rospy.init_node('webcam_publisher', anonymous=True)

    # Set required objects
    capture = cv.VideoCapture(0)
    bridge = CvBridge()
    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        ret, frame = capture.read()
        if ret == True:
            rospy.loginfo('publishing webcam frame...')
            publisher.publish(bridge.cv2_to_imgmsg(frame))
            rate.sleep()


if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass