import cv2
import os
import PIL
from PIL import Image

#reading image
path= 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\matchingtestdata\\test'

img1 = cv2.imread(path +'\\01.png')

img2 = cv2.imread(path +'\\05.png')

#(X, Y), (X + W, Y + H)
x1=865
y1=540
x2=1060
y2=800

cv2.rectangle(img1, (865, 540), (1060, 800), (255,0,0), 2)
#cv2.imshow('imgKp1', img1)

img = Image.open(path +'\\01.png')
im_crop = img.crop((x1, y1, x2, y2))
#im_crop.save('_0.png')

cv2.rectangle(img2, (875, 580), (1140, 1090), (255,0,0), 2)
#cv2.imshow('imgKp2', img2)

x1=875
y1=580
x2=1140
y2=1070

img = Image.open(path +'\\05.png')
im_crop = img.crop((x1, y1, x2, y2))
#im_crop.save('_1.png')

img1 = cv2.imread(path +'\\_0.png')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread(path +'\\_1.png')
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#default nfeatures=500
orb = cv2.ORB_create(nfeatures=10000)

#keypoints
kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

print(des1.shape)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if m.distance < 0.8*n.distance:
        good.append([m])

print(len(good))
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
img4 = cv2.drawMatchesKnn(gray1, kp1, gray2, kp2, good, None, flags=2)

imgKp1 = cv2.drawKeypoints(img1, kp1, None)
imgKp2 = cv2.drawKeypoints(img2, kp2, None)

#cv2.imshow('imgKp1', imgKp1)
#cv2.imshow('imgKp2', imgKp2)
cv2.imshow('img3', img3)
cv2.imshow('img4', img4)

filename = 'checks.jpg'
#cv2.imwrite(os.path.join(path , filename), img3)
cv2.waitKey(0)
