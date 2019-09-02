import os
import matplotlib.pyplot as plt 
import cv2
from PIL import Image
from matplotlib.widgets import RectangleSelector
from image_crawler import brands
from gen_annotations import write_xml

# Global variables
img = None
topleft = []
bottomright = []
object_list = []

image_folder = ""
savedir = './annotations'
obj = ""

def line_select_callback(clk, rls):
	global topleft
	global bottomright
	topleft.append((int(clk.xdata),int(clk.ydata)))
	bottomright.append((int(rls.xdata),int(rls.ydata)))
	object_list.append(obj)


def toggle_selector(event):
	toggle_selector.RS.set_active(True)

def onKeyPressed(event):
	global object_list
	global topleft
	global bottomright
	global img
	if event.key == 'q':
		if topleft == [] and bottomright == []:
			os.remove(img.path)
		else:
			write_xml(image_folder, img, object_list, topleft, bottomright, savedir)
		topleft = []
		bottomright = []
		object_list = []
		img = None
		plt.close()

if __name__ == '__main__':
	if not os.path.isdir(savedir):
		os.mkdir(savedir)
	for n, image_file in enumerate(os.scandir('./images/')):
		image_folder = './images/'
		if os.path.isfile(image_file.path) and '.DS' not in image_file.name:
			img = image_file
			fig, ax = plt.subplots(1)
			print(image_file.path)
			image = cv2.imread(image_file.path)
			if image is not None:
				image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
				ax.imshow(image)
				obj = image_file.name.split('_')[0]
				toggle_selector.RS = RectangleSelector(
					ax, line_select_callback, 
					drawtype='box', useblit=True,
					button=[1], minspanx=5, minspany=5,
					spancoords='pixels', interactive=True
					)

				bbox = plt.connect('key_press_event',toggle_selector)
				key = plt.connect('key_press_event', onKeyPressed)
				plt.show()
			else:
				os.remove(image_file.path)
