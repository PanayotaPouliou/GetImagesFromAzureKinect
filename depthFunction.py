import sys
sys.path.insert(1, 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\pyKinectAzure')

import numpy as np
#from pyKinectAzure import pyKinectAzure, _k4a, postProcessing
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
	a = 90
	b = 59

	fx = uo / math.tan(a/2)
	fy = vo / math.tan(b/2)

	xs,ys = subj_coordinates
	xo,yo = obj_coordinates

	Zs = depth.getpixel(subj_coordinates)

	Xs = (Zs*xs) / fx
	Ys = (Zs*ys) / fy
	
	Zo = depth.getpixel(obj_coordinates)

	Xo = (Zo*xo) / fx
	Yo = (Zo*yo) / fy

	A = (Xs,Ys,Zs)
	B = (Xo,Yo,Zo)

	D = math.sqrt((Xs-Xo)**2 + (Ys-Yo)**2 + (Zs-Zo)**2)

	return D , A, B

def get_Z(path, coordinates):

	depth= Image.open(path +'\\Smooth_mapped.png')

	z = depth.getpixel(coordinates)

	return z

def get_world_coord_one(path, subj_coordinates, obj_coordinates):

	depth= Image.open(path +'\\Smooth_mapped.png')

	width, height = depth.size

	uo = width/2
	vo = height/2

	#FOV given by the camera settings
	a = 90
	b = 59

	fx = uo / math.tan(a)
	fy = vo / math.tan(b)

	xs,ys = subj_coordinates
	xo,yo = obj_coordinates

	Zs = depth.getpixel(subj_coordinates)

	Xs = (xs - (Zs*uo)) / fx
	Ys = (ys - (Zs*vo)) / fy
	
	Zo = depth.getpixel(obj_coordinates)

	Xo = (xo - (Zo*uo)) / fx
	Yo = (yo - (Zo*vo)) / fy

	D = math.sqrt((Xs-Xo)**2 + (Ys-Yo)**2 + (Zs-Zo)**2)

	return D