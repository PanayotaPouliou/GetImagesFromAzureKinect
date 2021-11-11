from os import path
from getRealCoords import get_world_coord#, get_Z if we want !only! the depth
from PIL import Image

img_depth= Image.open('RealCoordinates\RWC_check\D_20211110113510.png')

subj_coordinates = 1464,464
obj_coordinates = 1145,752

#subj_depth = get_Z(img_depth, subj_coordinates)
#obj_depth = get_Z(img_depth, obj_coordinates)

D, A, B = get_world_coord(img_depth, subj_coordinates, obj_coordinates)

print(D,A,B)