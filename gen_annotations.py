import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET 
from image_crawler import brands 

# folder: folder from where comes the image 
# img: the image name
# objects: classes or categories
# topleft: list of topleft of each bounding box
# bottomright: list of bottomright of each bounding box
# savedir: where to save the xml

def write_xml(folder, img, objects, topleft, bottomright, savedir):
	image = cv2.imread(img.path)
	height, width, depth = image.shape

	# Building this xml structure
	"""
	<annotation>
		<folder>VOC2007</folder>
		<filename>1.jpg</filename>
		<source>
			<database>The VOC2007 Database</database>
			<annotation>PASCAL VOC2007</annotation>
			<image>flickr</image>
			<flickrid>336426776</flickrid>
		</source>
		<owner>
			<flickrid>Elder Timothy Chaves</flickrid>
			<name>Tim Chaves</name>
		</owner>
		<size>
			<width>500</width>
			<height>375</height>
			<depth>3</depth>
		</size>
		<segmented>0</segmented>
		<object>
			<name>person</name>
			<pose>Left</pose>
			<truncated>0</truncated>
			<difficult>0</difficult>
			<bndbox>
				<xmin>135</xmin>
				<ymin>25</ymin>
				<xmax>236</xmax>
				<ymax>188</ymax>
			</bndbox>
		</object>
		<object>
			<name>bicycle</name>
			<pose>Left</pose>
			<truncated>0</truncated>
			<difficult>0</difficult>
			<bndbox>
				<xmin>95</xmin>
				<ymin>85</ymin>
				<xmax>232</xmax>
				<ymax>253</ymax>
			</bndbox>
		</object>
	</annotation>

	"""

	annotation = ET.Element('annotation')
	ET.SubElement(annotation,'folder').text = folder
	ET.SubElement(annotation,'filename').text = img.name
	ET.SubElement(annotation,'segmented').text = '0'
	size = ET.SubElement(annotation,'size')
	ET.SubElement(size,'width').text = str(width)
	ET.SubElement(size,'height').text = str(height)
	ET.SubElement(size,'depth').text = str(depth)

	# Create Object elements
	for object_, tl, br in zip(objects, topleft, bottomright):
		object_tag = ET.SubElement(annotation,'object')
		ET.SubElement(object_tag,'name').text = object_
		ET.SubElement(object_tag,'pose').text = 'unspecified'
		ET.SubElement(object_tag,'truncated').text = '0'
		ET.SubElement(object_tag,'difficult').text = '0'
		bndbox_tag = ET.SubElement(object_tag,'bndbox')
		ET.SubElement(bndbox_tag,'xmin').text = str(tl[0])
		ET.SubElement(bndbox_tag,'ymin').text = str(tl[1])
		ET.SubElement(bndbox_tag,'xmax').text = str(br[0])
		ET.SubElement(bndbox_tag,'ymax').text = str(br[1])

	xml_str = ET.tostring(annotation)
	root = etree.fromstring(xml_str)
	xml_str = etree.tostring(root, pretty_print=True)
	if 'png' in img.name:
		save_path = os.path.join(savedir, img.name.replace('.png', '_png.xml'))
	elif 'jpg' in img.name:
		save_path = os.path.join(savedir, img.name.replace('.jpg', '_jpg.xml'))
	elif 'jpeg' in img.name:
		save_path = os.path.join(savedir, img.name.replace('.jpeg', '_jpeg.xml'))
	with open(save_path, 'wb') as temp_xml:
		temp_xml.write(xml_str)
	return xml_str





