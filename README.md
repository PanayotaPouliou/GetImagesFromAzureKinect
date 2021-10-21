# Getting real world coordinates
using pyKinectAzure Library to capture data

## Prerequisites
* [Azure-Kinect-Sensor-SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK): required to build this library.
  To use the SDK, refer to the installation instructions [here](https://github.com/microsoft/Azure-Kinect-Sensor-SDK).
* **ctypes**: required to read the library.
* **numpy**: required for the matrix calculations
* **opencv-python**: Required for the image transformations and visualization.

## How to use this library
follow the given instruction at the following repository
https://github.com/ibaiGorordo/pyKinectAzure

## The functions
get_data: allows you to open Kinect, modify camera configuarations, take shots (rgb, depth) and exports transformed depth map to the rgb image.
          it is also smoothening the edges of the depth map and it gives ou the option to prin the depth map in color for a better unerstanding of it.
          
          (https://github.com/PanayotaPouliou/GetImagesFromAzureKinect/blob/master/ExamplePictures/Smooth_mapped_1.png)
          (https://github.com/PanayotaPouliou/GetImagesFromAzureKinect/blob/master/ExamplePictures/Smooth_mapped_10.png)
          
get_world_coord: takes as input two pixel coordinates A(xa,ya) and B(xb, yb) and gives as an output the real world coordinates with the camera being the O(0,0,0).
                 moreover it returns the actual distance between A and B in mm.
                 
get_Z: Gives the pixel value which is equal with the distance between a point in the real world and the camera (a.k.a the depth.)


