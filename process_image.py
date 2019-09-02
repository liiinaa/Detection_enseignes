import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt 
import os

# Get the bounding box with the max confidence 
def getMax(arr, prop):
	max_object = arr[0]
	for i in range(0,len(arr)):
		if (max_object) and arr[i][prop] > max_object[prop]:
			max_object = arr[i]
	return max_object

# model
options = {
	'model': 'cfg/tiny-yolo-voc-4c.cfg',
	'load': -1 ,
	'threshold': 0.4,
	'gpu':0.0
}

tfnet = TFNet(options)

image_directory="./test_img/"

for image_file in os.listdir(image_directory):
	print(image_file)
	if image_file.endswith(".png") or image_file.endswith(".jpg") or image_file.endswith(".jpeg"):
		# predictions
		img = cv2.imread(image_directory+image_file, cv2.IMREAD_COLOR)
		result = tfnet.return_predict(img)
		# drawing bounding box with text
		print(result)
		# Draw the bounding box of all objects
		for i in range(0,len(result)):
			topleft = (result[i]['topleft']['x'],result[i]['topleft']['y'])
			bottomright = (result[i]['bottomright']['x'],result[i]['bottomright']['y'])
			label = result[i]['label']
			img = cv2.rectangle(img, topleft, bottomright, (255,0,0), 3)
			img = cv2.putText(img, label, topleft, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
		cv2.imwrite("./test_img/out/"+image_file, img)
		"""
		# Draw the bounding box of a single object
		max_object = getMax(result,'confidence')

		topleft = (max_object['topleft']['x'],max_object['topleft']['y'])
		bottomright = (max_object['bottomright']['x'],max_object['bottomright']['y'])
		label = max_object['label']
		img = cv2.rectangle(img, topleft, bottomright, (255,0,0), 3)
		img = cv2.putText(img, label, topleft, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
		"""
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		plt.imshow(img)
		plt.show()
