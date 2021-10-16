# ROS_Packages
My 'Robotics Operating System' Packages

## Camera
* Provides imaqge detection and recognition + bounding boxes with text descriptions
* 3 Nodes:
** webcam_pub: utilising opencv VideoCapture, converts opencv webcam frames to ROS Image message type and publishes to the video_frames_raw Topic.
** webcam_process: receives Image messages from video_frame_raw Topic. Processes object detection and recognition utilising Tensorflow Lite SSD Mobilenet v1. Adds bounding boxes and description labels and publishes message to the video_frames_processed Topic.
