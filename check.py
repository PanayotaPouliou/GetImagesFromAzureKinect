import cv2
from depthFunction import get_data
import PIL
from PIL import Image


color, depth_1 = get_data('C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\dData', 'no', 10)


#cv2.imshow('image:color', color)
#cv2.waitKey(0)
##cv2.imshow('image:colored_depth', depth_1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

coordinates = 100, 100
raw_depth = depth_1.getpixel(coordinates)

print(raw_depth)