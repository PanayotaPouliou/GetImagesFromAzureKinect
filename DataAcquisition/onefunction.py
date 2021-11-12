import sys
# sys.path.insert(1, '/workspaces/sg_benchmark/pyKinectAzure')
import pyKinectAzure
from pyKinectAzure import pyKinectAzure, _k4a, postProcessing
import _k4a
import csv
import cv2

import os
import os.path
from PIL import Image
import numpy as np
import pendulum
import time

def get_metadata(path, path_c, path_d, dt, filename):
    newpath = path + '\\' + filename + '.csv'

    file_exists = os.path.exists(newpath)
    # open images
    im_c = Image.open(path_c)
    im_d = Image.open(path_d)

    # get image's width and height
    width_c, height_c = im_c.size
    width_d, height_d = im_d.size

    # get RGB image format
    format_c = im_c.format
    format_d_c = im_c.format_description
    format_d_c = format_d_c.replace((format_c + ' '), "")

    # get D image format
    format = im_d.format
    format_d = im_d.format_description
    format_d = format_d.replace((format + ' '), "")

    im_c.close()
    im_d.close()


    if file_exists == True:

        # open the file in the write mode
        with open(newpath, 'a') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write the rows to the csv file for each one of the 2 generated images
            name_c = 'RGB_' + dt
            row = [name_c, width_c, height_c,
                   dt, format_c, format_d_c, path_c]
            writer.writerow(row)
            name_d = 'D_' + dt
            row = [name_d, width_d, height_d,
                   dt, format, format_d, path_d]
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
        name_c = 'RGB_' + dt
        row = [name_c, width_c, height_c,
               dt, format_c, format_d_c, path_c]
        writer.writerow(row)
        name_d = 'D_' + dt
        row = [name_d, width_d, height_d,
               dt, format, format_d, path_d]
        writer.writerow(row)

        # close the file
        f.close()
    

# path: where to save the output, w: write 'color' for colored_depth / anything else for regular, maximum_hole_size: the bigger number-the better
# filename: the name of the CSV file that will have the metadata of the images, fr_number: the numbers of the frame that we want, timeframe: how many seconds should wait for each capture
def get_data(path, w, maximum_hole_size, filename,fr_number, timeframe):
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
    #print(device_config)

    # Start cameras using modified configuration
    pyK4A.device_start_cameras(device_config)

    ####### loop starts here #######
    k = 0
    while True:

        for i in range(0,fr_number):
            #wait until the time of the next capture
            time.sleep(timeframe)

            # Get capture
            pyK4A.device_get_capture()

            # Get time of capture
            dt = pendulum.now("Europe/Copenhagen")
            dt = dt.format("YMMDDHHmmss")

            # Get the depth image from the capture
            depth_image_handle = pyK4A.capture_get_depth_image()

            # Get the color image from the capture
            color_image_handle = pyK4A.capture_get_color_image()

            if depth_image_handle and color_image_handle:

                # Read and convert the image data to numpy array:
                color_image = pyK4A.image_convert_to_numpy(
                    color_image_handle)[:, :, :3]

                # Transform the depth image to the color format
                transformed_depth_image = pyK4A.transform_depth_to_color(depth_image_handle, color_image_handle)

                # Smooth the image using Navier-Stokes based inpainintg. maximum_hole_size defines
                # the maximum hole size to be filled, bigger hole size will take longer time to process
                smoothed_depth_image = postProcessing.smooth_depth_image(
                    transformed_depth_image, maximum_hole_size)

                # Saving the edited depth image
                # cv2.imwrite(os.path.join(path , filename), transformed_depth_image)
                if w == 'color':

                    # Convert depth image (mm) to color, the range needs to be reduced down to the range (0,255)
                    smooth_depth_color_image = cv2.applyColorMap(
                        np.round(smoothed_depth_image / 30).astype(np.uint8), cv2.COLORMAP_JET)

                    # Construct names
                    SMC_name = 'D_' + dt + '.png'
                    RGB_name = 'RGB_' + dt + '.jpg'

                    # Saving the color and colored depth image
                    cv2.imwrite(os.path.join(path, RGB_name), color_image)
                    cv2.imwrite(os.path.join(path, SMC_name),
                                smooth_depth_color_image)

                    #Release the color and depth image handle
                    pyK4A.image_release(depth_image_handle)
                    pyK4A.image_release(color_image_handle)

                else:
                    RGB_name = 'RGB_' + dt + '.jpg'
                    SD_name = 'D_' + dt + '.png'

                    # Saving the color and depth image
                    cv2.imwrite(os.path.join(path, RGB_name), color_image)
                    cv2.imwrite(os.path.join(path, SD_name), smoothed_depth_image)

                    #Release the color and depth image handle
                    pyK4A.image_release(depth_image_handle)
                    pyK4A.image_release(color_image_handle)

                    #find image paths (RGB and D)
                    path_c = path + '\\' + RGB_name
                    path_d = path + '\\' + SD_name

                    #Create the CSV file with the metadata of the pictures
                    get_metadata(path, path_c, path_d, dt, filename)

                if i == (fr_number-1):
                    k = 1

            pyK4A.capture_release()

        if k == 1:    # Esc key to stop
            break

    pyK4A.device_stop_cameras()
    pyK4A.device_close()


def create_folder(path, folderName):
    newpath = path + '\\' + folderName
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    # else:
        # print('The name alreasy exists, please, provide a different folder name.')

    return newpath
