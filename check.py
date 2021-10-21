from depthFunctions import get_world_coord, get_Z
from capture import get_data

path= 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\dData'
#get_data(path, 'no', 10)

subj_coordinates = 832,151
obj_coordinates = 1152,151

#subj_depth = get_Z(path, subj_coordinates)
#obj_depth = get_Z(path, obj_coordinates)

D, A, B = get_world_coord(path, subj_coordinates, obj_coordinates)

print(D,A,B)