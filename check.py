import cv2
import os
from depthFunction import get_world_coord, get_Z
from depth_prior import get_data
import PIL
from PIL import Image
import math
import numpy as np


path= 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\dData'
#get_data(path, 'no', 10)

subj_coordinates = 519,216
obj_coordinates = 546,545

subj_depth = get_Z(path, subj_coordinates)
obj_depth = get_Z(path, obj_coordinates)

D, A, B = get_world_coord(path, subj_coordinates, obj_coordinates)

#print(subj_depth, obj_depth, d)
print(D,A,B)