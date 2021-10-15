import cv2
from depthFunction import get_data


color, depth = get_data('C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\dData', 'color', 10)


cv2.imshow('image:color', color)
cv2.waitKey(0)
cv2.imshow('image:colored_depth', depth)
cv2.waitKey(0)
cv2.destroyAllWindows() 
