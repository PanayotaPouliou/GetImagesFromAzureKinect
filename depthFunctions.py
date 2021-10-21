import sys
sys.path.insert(1, 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\pyKinectAzure')

import numpy as np
from pyKinectAzure import pyKinectAzure, _k4a, postProcessing
import cv2
import os
import PIL
from PIL import Image
import math

def get_world_coord(path, subj_coordinates, obj_coordinates):

	depth= Image.open(path +'\\Smooth_mapped.png')

	width, height = depth.size

	uo = width/2
	vo = height/2

	#FOV given by the depth camera settings
	a = 90*math.pi/180
	b = 59*math.pi/180

	fx = uo / math.tan(a/2)
	fy = vo / math.tan(b/2)

	xs,ys = subj_coordinates
	xo,yo = obj_coordinates
	
	xss= xs - uo
	yss= ys -vo
	xoo= xo - uo
	yoo= yo - vo

	Zs = depth.getpixel(subj_coordinates)

	Xs = (Zs*xss) / fx
	Ys = -(Zs*yss) / fy
	
	Zo = depth.getpixel(obj_coordinates)

	Xo = (Zo*xoo) / fx
	Yo = -(Zo*yoo) / fy

	A = (Xs,Ys,Zs)
	B = (Xo,Yo,Zo)

	D = math.sqrt((Xs-Xo)**2 + (Ys-Yo)**2 + (Zs-Zo)**2)

	return D , A, B

def get_Z(path, coordinates):

	depth= Image.open(path +'\\Smooth_mapped.png')

	z = depth.getpixel(coordinates)

	return z

#path: where to save the output, w: write 'color' for colored_depth / anything else for regular, maximum_hole_size: the bigger number-the better
def get_data(path, w, maximum_hole_size):
	# Path to the module
	modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

	# Open device
	pyK4A.device_open()

	# Modify camera configuration
	device_config = pyK4A.config
	device_config.color_format = _k4a.K4A_IMAGE_FORMAT_COLOR_BGRA32
	device_config.color_resolution = _k4a.K4A_COLOR_RESOLUTION_1080P
	device_config.depth_mode = _k4a.K4A_DEPTH_MODE_WFOV_2X2BINNED
	print(device_config)

	# Start cameras using modified configuration
	pyK4A.device_start_cameras(device_config)
	
	k = 0
	while True:
		# Get capture
		pyK4A.device_get_capture()

		# Get the depth image from the capture
		depth_image_handle = pyK4A.capture_get_depth_image()

		# Get the color image from the capture
		color_image_handle = pyK4A.capture_get_color_image()

		# Check the image has been read correctly
		if depth_image_handle and color_image_handle:

			# Read and convert the image data to numpy array:
			color_image = pyK4A.image_convert_to_numpy(color_image_handle)[:,:,:3]

			# Transform the depth image to the color format
			transformed_depth_image = pyK4A.transform_depth_to_color(depth_image_handle,color_image_handle)

			# Smooth the image using Navier-Stokes based inpainintg. maximum_hole_size defines 
			# the maximum hole size to be filled, bigger hole size will take longer time to process
			smoothed_depth_image = postProcessing.smooth_depth_image(transformed_depth_image, maximum_hole_size)
			
			# Convert depth image (mm) to color, the range needs to be reduced down to the range (0,255)
			smooth_depth_color_image = cv2.applyColorMap(np.round(smoothed_depth_image/30).astype(np.uint8), cv2.COLORMAP_JET)

			# Filename
			#filename = 'mapped.png'
			filename_1 = 'Smooth_mapped.png'
			filename_2 = 'color.png'
			filename_3 = 'smooth_color.png'

			# Saving the edited depth image
			#cv2.imwrite(os.path.join(path , filename), transformed_depth_image)
			if w =='color':
				# Saving the color and colored depth image
				cv2.imwrite(os.path.join(path , filename_3), smooth_depth_color_image)
				cv2.imwrite(os.path.join(path , filename_2), color_image)

				#read images
				color= cv2.imread(path +'\\color.png')
				colored_depth= cv2.imread(path +'\\smooth_color.png')

				#return images
				return(color, colored_depth)
				
			else:
				# Saving the color and depth image
				cv2.imwrite(os.path.join(path , filename_2), color_image)
				cv2.imwrite(os.path.join(path , filename_1), smoothed_depth_image) 

				#read images
				color= cv2.imread(path +'\\color.png')
				depth= cv2.imread(path +'\\Smooth_mapped.png')

				#return images
				return(color, depth)	

			k = 1

			pyK4A.image_release(depth_image_handle)
			pyK4A.image_release(color_image_handle)

		pyK4A.capture_release()

		if k==1:    # Esc key to stop
			break

	pyK4A.device_stop_cameras()
	pyK4A.device_close()