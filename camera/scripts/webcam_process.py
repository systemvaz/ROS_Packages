#!/usr/bin/env python3

import os
import rospy
import rospkg
import cv2 as cv
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from tflite_runtime.interpreter import Interpreter


rospack = rospkg.RosPack()
package_dir = rospack.get_path('camera')
publisher = rospy.Publisher('video_frames_processed', Image, queue_size=24)

# Tensorflow Lite model declarations
model_path_tf = os.path.join(package_dir, "models/lite-model_ssd_mobilenet_v1_1_metadata_2.tflite")
label_path_tf = os.path.join(package_dir, "models/labelmap.txt")

interpreter = Interpreter(model_path=model_path_tf)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

labels = []
with open(label_path_tf, 'r') as f:
    for line in f:
        line = line.rstrip()
        labels.append(line)

bounding_box_colours = np.random.uniform(255, 0, size=(len(labels), 3))        


# TF Lite detection and recognition
def process_tflite(frame):
    videoHeight = frame.shape[0]
    videoWidth = frame.shape[1]
    frame_cpy = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame_cpy = cv.resize(frame_cpy, (width, height))
    input_image = np.expand_dims(frame_cpy, axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    for i in range(len(scores)):
        if scores[i] >= 0.50:
            ymin = int(max(1, (boxes[i][0] * videoHeight)))
            xmin = int(max(1, (boxes[i][1] * videoWidth)))
            ymax = int(min(videoHeight, (boxes[i][2] * videoHeight)))
            xmax = int(min(videoWidth, (boxes[i][3] * videoWidth)))

            (txtW, txtH), _ = cv.getTextSize(labels[int(classes[i])], cv.FONT_HERSHEY_SIMPLEX, 0.8, 1)
            cv.rectangle(frame, (xmin, ymin - 30), (xmin + txtW + 5, ymin), bounding_box_colours[int(classes[i])], -1)
            cv.rectangle(frame, (xmin, ymin), (xmax, ymax), bounding_box_colours[int(classes[i])], 2)
            cv.putText(frame, labels[int(classes[i])], (xmin + 2, ymin - 5), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    return frame


def callback(data):
    bridge = CvBridge()
    rospy.loginfo('processing webcam frame')
    current_frame = bridge.imgmsg_to_cv2(data)
    frame = process_tflite(current_frame)
    publisher.publish(bridge.cv2_to_imgmsg(frame))


def receive_message():
    rospy.init_node('webcam_processor', anonymous=True)
    rospy.Subscriber('video_frames_raw', Image, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        receive_message()
    except rospy.ROSInterruptException:
        pass
