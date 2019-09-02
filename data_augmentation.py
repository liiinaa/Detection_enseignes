import numpy as np
import os
import cv2
import shutil
import xml.etree.ElementTree as ET

# Adds brightness to the image
def increase_brightness(image, value=30):
	image_brightness = image.copy()
	hsv = cv2.cvtColor(image_brightness, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)

	lim = 255 - value
	v[v > lim] = 255
	v[v <= lim] += value

	final_hsv = cv2.merge((h, s, v))
	image_brightness = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

	return image_brightness

# Adds salt and pepper to the image
def add_salt_pepper_noise(image):
	image_saltPepper = image.copy()
	row, col, _ = image_saltPepper.shape
	salt_vs_pepper = 0.2
	amount = 0.004
	num_salt = np.ceil(amount * image_saltPepper.size * salt_vs_pepper)
	num_pepper = np.ceil(amount * image_saltPepper.size * (1.0 - salt_vs_pepper))
	
	# Add Salt noise
	coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image_saltPepper.shape]
	image_saltPepper[coords[0], coords[1], :] = 255

	# Add Pepper noise
	coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image_saltPepper.shape]
	image_saltPepper[coords[0], coords[1], :] = 0
	return image_saltPepper

# Adds a blur to the image (image smoothing)
def averaging_filter(image):
	image_averaging = image.copy()
	blur = cv2.blur(image_averaging,(5,5))
	return blur

# Creates the three new images
def add_filters(image_object):
	image = cv2.imread(image_object.path)

	image_saltPepper = add_salt_pepper_noise(image)
	cv2.imwrite('./images/'+image_object.name+'_saltAndPepper.jpg',image_saltPepper)

	image_brightness = increase_brightness(image,50)
	cv2.imwrite('./images/'+image_object.name+'_brightness.jpg',image_brightness)

	image_averaging = averaging_filter(image)
	cv2.imwrite('./images/'+image_object.name+'_averaging.jpg',image_averaging)

# Generates annotations of those three images
def generate_annotations(base_name, image_file):

	if 'png' in image_file.name:
		ending = 'png'
	elif 'jpg' in image_file.name:
		ending = 'jpg'
	elif 'jpeg' in image_file.name:
		ending = 'jpeg'

	# Locations of annotations of these three images
	destination_brightness = './annotations/'+image_file.name.split('.')[0]+'_'+ending+'_brightness.xml'
	destination_averaging = './annotations/'+image_file.name.split('.')[0]+'_'+ending+'_averaging.xml'
	destination_saltAndPepper = './annotations/'+image_file.name.split('.')[0]+'_'+ending+'_saltAndPepper.xml'

	# copying the XML source files 
	shutil.copy(base_name+'.xml',destination_brightness)
	shutil.copy(base_name+'.xml',destination_averaging)
	shutil.copy(base_name+'.xml',destination_saltAndPepper)

	# Changing 'filename' tag in the XML
	tree = ET.parse(base_name+'.xml')
	root = tree.getroot()
	print(root[1].tag,root[1].text)

	root[1].text = image_file.name.split('.')[0]+'_brightness.'+ending
	tree.write(destination_brightness)
	root[1].text = image_file.name.split('.')[0]+'_averaging.'+ending
	tree.write(destination_averaging)
	root[1].text = image_file.name.split('.')[0]+'_saltAndPepper.'+ending
	tree.write(destination_saltAndPepper)

if __name__ == '__main__':
	for n, image_file in enumerate(os.scandir('./images/')):
		if not str(image_file.name).startswith('.'):
			add_filters(image_file)
			if 'png' in image_file.name:
				ending = 'png'
			elif 'jpg' in image_file.name:
				ending = 'jpg'
			elif 'jpeg' in image_file.name:
				ending = 'jpeg'
			print(image_file.name)
			base_name = './annotations/'+image_file.name.split('.')[0]+'_'+ending
			generate_annotations(base_name, image_file)
