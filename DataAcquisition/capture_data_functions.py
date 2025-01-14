import sys
sys.path.insert(1, 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\pyKinectAzure')
from pyKinectAzure import pyKinectAzure, _k4a, postProcessing
import csv
import cv2
import time
import os
import os.path
from PIL import Image
import numpy as np


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
			filename_2 = 'color.jpg'
			filename_3 = 'smooth_color.png'

			# Saving the edited depth image
			#cv2.imwrite(os.path.join(path , filename), transformed_depth_image)
			if w =='color':
				# Saving the color and colored depth image
				cv2.imwrite(os.path.join(path , filename_3), smooth_depth_color_image)
				cv2.imwrite(os.path.join(path , filename_2), color_image)

				#read images
				color= cv2.imread(path +'\\color.jpg')
				colored_depth= cv2.imread(path +'\\smooth_color.png')

				#return images
				return(color, colored_depth)
				
			else:
				# Saving the color and depth image
				cv2.imwrite(os.path.join(path , filename_2), color_image)
				cv2.imwrite(os.path.join(path , filename_1), smoothed_depth_image) 

				#read images
				color= cv2.imread(path +'\\color.jpg')
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

    #print('camera closed')


def closeCamera():
    # Path to the module
	modulePath = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll'

	# Initialize the library with the path containing the module
	pyK4A = pyKinectAzure(modulePath)

    #pyK4A.device_stop_cameras()
	pyK4A.device_close()



def create_folder(path, folderName):
    newpath = path + '\\' + folderName
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    #else:
        #print('The name alreasy exists, please, provide a different folder name.')

    return newpath


def timestamp(f_path, filename):
    # Getting the path of the file
    #f_path = 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\filesaving'
    path_c = f_path + '\\color.jpg'
    path_d = f_path + '\\Smooth_mapped.png'

    im_c = Image.open(path_c)
    im_d = Image.open(path_d)

    #get image's width and height
    width_c, height_c = im_c.size
    width_d, height_d = im_d.size

    #get image format
    format_c = im_c.format
    format_d_c = im_c.format_description
    format_d_c = format_d_c.replace((format_c + ' '), "")

    format = im_d.format
    format_d = im_d.format_description
    format_d = format_d.replace((format + ' '), "")

    im_c.close()
    im_d.close()

    # Obtaining the creation time (in seconds)
    # of the file/folder (datatype=int)
    t = os.path.getctime(path_c)
    t2 = os.path.getctime(path_d)

    # Converting the time to an epoch string
    # (the output timestamp string would
    # be recognizable by strptime() without
    # format quantifers)
    t_str = time.ctime(t)
    t_str2 = time.ctime(t2)

    # Converting the string to a time object
    t_obj = time.strptime(t_str)
    t_obj2 = time.strptime(t_str2)

    # Transforming the time object to a timestamp
    # of Year_Month_Day_Hour_Min_Sec : 20211104173745
    form_t = time.strftime("%Y%m%d%H%M%S", t_obj)
    form_t2 = time.strftime("%Y%m%d%H%M%S", t_obj2)

    # Renaming the filename to its timestamp plus RGB or D depending on the img type
    os.rename(
        path_c, os.path.split(path_c)[0] + '\\' + 'RGB_' + form_t + os.path.splitext(path_c)[1])

    os.rename(
        path_d, os.path.split(path_d)[0] + '\\' + 'D_' + form_t2 + os.path.splitext(path_d)[1])


    newpath = f_path + '\\' + filename + '.csv'

    file_exists = os.path.exists(newpath)



    if file_exists==True:

        # open the file in the write mode
        with open(newpath,'a') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write the rows to the csv file for each one of the 2 generated images
            name_c = 'RGB_' + form_t
            row = [name_c, width_c, height_c,
                  form_t, format_c, format_d_c, path_c]
            writer.writerow(row)
            name_d = 'D_' + form_t2
            row = [name_d, width_d, height_d,
                  form_t2, format, format_d, path_d]
            writer.writerow(row)

    else:
        # open the file in the write mode
        f = open(newpath, 'w')

        # create the csv writer
        writer = csv.writer(f)
        # Create the header of the csv file
        head = ['file_name', 'width', 'height',
                'timestamp', 'format', 'f_description', 'file']

        writer.writerow(head)

        # write the rows to the csv file for each one of the 2 generated images
        name_c = 'RGB_' + form_t
        row = [name_c, width_c, height_c,
              form_t, format_c, format_d_c, path_c]
        writer.writerow(row)
        name_d = 'D_' + form_t2
        row = [name_d, width_d, height_d,
              form_t2, format, format_d, path_d]
        writer.writerow(row)

        # close the file
        f.close()

    return form_t, form_t2


def captureData(in_path, fol_name, fil_name):

    #New Folder Creation
    path = create_folder(in_path, fol_name)

    #Save files in the created folder
    get_data(path, 'no', 10)

    #renames files in the path with their timestamp
    timestamp(path, fil_name)