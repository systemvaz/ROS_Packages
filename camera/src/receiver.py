import cv2 as cv
import imagezmq

image_hub = imagezmq.ImageHub()

while True:
    srv_name, frame = image_hub.recv_image()
    cv.namedWindow("ROS Network Video Stream", 0)
    cv.resizeWindow("ROS Network Video Stream", 640, 480)
    cv.imshow("ROS Network Video Stream", frame)
    image_hub.send_reply(b'OK')
    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()