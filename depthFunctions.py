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

	#open the transformed, smoothed depth image
	depth= Image.open(path +'\\Smooth_mapped.png')

	width, height = depth.size

	uo = width/2
	vo = height/2

	#FOV given by the depth camera settings
	a = 90*math.pi/180
	b = 59*math.pi/180

	fx = uo / math.tan(a/2)
	fy = vo / math.tan(b/2)

	#Get the pixel coordinates of the objects that we want to get their real world coords
	xs,ys = subj_coordinates
	xo,yo = obj_coordinates
	
	#Swift the 0,0 from top left corner to center of the picture (where the camera is)
	xss= xs - uo
	yss= ys -vo
	xoo= xo - uo
	yoo= yo - vo

	#Get depth of pixels
	Zs = depth.getpixel(subj_coordinates)
	Zo = depth.getpixel(obj_coordinates)

	#calculate real world coordinates
	Xs = (Zs*xss) / fx
	Ys = -(Zs*yss) / fy

	Xo = (Zo*xoo) / fx
	Yo = -(Zo*yoo) / fy

	#The final coords
	A = (Xs,Ys,Zs)
	B = (Xo,Yo,Zo)

	#Calculate the distance between the two points in the real world
	D = math.sqrt((Xs-Xo)**2 + (Ys-Yo)**2 + (Zs-Zo)**2)

	#This function returns Distance, Subject_coords, Object_coords
	return D , A, B

def get_Z(path, coordinates):

	depth= Image.open(path +'\\Smooth_mapped.png')

	z = depth.getpixel(coordinates)

	return z