from os import path
from getRealCoords import get_world_coord#, get_Z if we want !only! the depth
from PIL import Image

img_depth= Image.open('C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\filesaving\\CITA\\2021-11-01 11꞉29꞉44 d.png')

subj_coordinates = 832,151
obj_coordinates = 1152,151

#subj_depth = get_Z(img_depth, subj_coordinates)
#obj_depth = get_Z(img_depth, obj_coordinates)

D, A, B = get_world_coord(img_depth, subj_coordinates, obj_coordinates)

print(D,A,B)