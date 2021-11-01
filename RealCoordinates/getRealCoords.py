from PIL import Image
import math

def get_world_coord(img_depth, subj_coordinates, obj_coordinates):

	width, height = img_depth.size

	uo = width/2
	vo = height/2

	#FOV (90, 59) given by the depth camera settings
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
	Zs = img_depth.getpixel(subj_coordinates)
	Zo = img_depth.getpixel(obj_coordinates)

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


#A function getting the depth value from the depthmap
def get_Z(img_depth, coordinates):

	z = img_depth.getpixel(coordinates)
	return z