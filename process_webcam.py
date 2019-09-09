import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

# model
options = {
	'model': 'cfg/tiny-yolo-voc-3c.cfg',
	'load': -1,
	'threshold': 0.1,
	'gpu':0.0
}

tfnet = TFNet(options)

colors = [tuple(255 * np.random.rand(3)) for i in range(3)]

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,800)
fps = capture.get(cv2.CAP_PROP_FPS)
print(fps)

while True:
	stime = time.time()
	ret, frame = capture.read()
	results = tfnet.return_predict(frame)
	if ret:	# if video is playing
		# different bbox's colors in a frame
		for result in results: # for each couple of color and result
			topleft = (result['topleft']['x'],result['topleft']['y'])
			bottomright = (result['bottomright']['x'],result['bottomright']['y'])
			label = result['label']
			if label == "Carrefour":
				frame = cv2.rectangle(frame, topleft, bottomright, colors[0], 7)
			if label == "Auchan":
				frame = cv2.rectangle(frame, topleft, bottomright, colors[1], 7)
			if label == "Decathlon":
				frame = cv2.rectangle(frame, topleft, bottomright, colors[2], 7)
			confidence = result['confidence']
			text = '{}: {:.0f}%'.format(label,confidence * 100)
			# image - text - location - font - ... - color of the font - ...
			frame = cv2.putText(frame, text, topleft, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
			frame = cv2.resize(frame,(1400,620))
		cv2.imshow('frame',frame)
		#video.write(frame)
		print('FPS {:.1f}'.format(1/(time.time() - stime)))
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		capture.release()
		cv2.destroyAllWindows()
		break