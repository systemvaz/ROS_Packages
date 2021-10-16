# ROS_Packages
My 'Robotics Operating System' Packages

## Camera
* Provides imaqge detection and recognition + bounding boxes with text descriptions
* 3 Nodes:
  * scripts/webcam_pub.py: Utilising opencv VideoCapture, converts opencv webcam frames to ROS Image message type and publishes to the video_frames_raw Topic.
  * scripts/webcam_process.py: Subscribes to Image messages from video_frame_raw Topic. Processes object detection and recognition utilising Tensorflow Lite SSD Mobilenet v1. Adds bounding boxes and description labels and publishes message to the video_frames_processed Topic.
  * scripts/webcam_view.py: Subscribes to Image meessages from video_frames_processed Topic. Utilising ImageZMQ sends images over network to IP defined in ImageSender method.
 * Additional:
  * /src/receiver.py: Run this on machine with IP defined in ImageSend method in webcam_view.py to view final webcam stream.
  * /models/: Tensorflow Lite model and classes txt file.

<img src="https://github.com/systemvaz/ROS_Packages/blob/master/camera/src/rosgraph.png" height=150%>
<img src="https://github.com/systemvaz/ROS_Packages/blob/master/camera/src/ros_img_detect.JPG" width=50% height=50%>
