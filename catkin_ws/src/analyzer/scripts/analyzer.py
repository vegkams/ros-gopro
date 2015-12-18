import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from rect.rect import Rect

class Analyzer:
	def __init__(self):
		self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
		self.bridge = CvBridge()
		self.anglesInImage = 127

	def callbackImage(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)
		
		
	def listener(self):
		rospy.init_node('AnalyzerGoPro', anonymous=True)

		rospy.Subscriber("FluxGoPro", Image, callbackImage)

		rospy.spin()
	
	def test(self):
		img = cv2.imread('test.jpg')
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		(width, height, _) = img.shape
		faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
			rectangle = Rect((x,y,w,h))
			(xCent, yCent) = rectangle.get_center()

			if xCent < (width/2):
				print "left"
			elif if xCent > (width/2):
				print "right"
			if yCent < (height/2):
				print "bottom"
			elif if yCent > (height/2):
				print "top"

			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			eyes = self.eye_cascade.detectMultiScale(roi_gray)
			
			if len(eyes) >= 2 :
				cv2.putText(img,"Face detected", (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))

		cv2.imshow('img',img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

if __name__ == '__main__':
    anal = Analyzer()
    anal.test()

