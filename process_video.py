import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

# model
options = {
	'model': 'cfg/yolo.cfg',
	'load': 'bin/yolov2.weights',
	'threshold': 0.4,
	'gpu':0.0
}

tfnet = TFNet(options)

capture = cv2.VideoCapture('video.mp4')

colors = [tuple(255 * np.random.rand(3)) for i in range(20)]

while(capture.isOpened()):
	stime = time.time()
	ret, frame = capture.read()
	results = tfnet.return_predict(frame)
	if ret:	# if video is playing
		for color, result in zip(colors,results): # for each couple of color and result
			topleft = (result['topleft']['x'],result['topleft']['y'])
			bottomright = (result['bottomright']['x'],result['bottomright']['y'])
			label = result['label']
			frame = cv2.rectangle(frame, topleft, bottomright, (0,0,255), 7)
			# image - text - location - font - ... - color of the font - ...
			frame = cv2.putText(frame, label, topleft, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else: 
		capture.release()
		cv2.destroyAllWindows()
		break

