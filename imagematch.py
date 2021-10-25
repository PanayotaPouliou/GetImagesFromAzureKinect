import cv2
import os

#reading image
path= 'C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\dData'

img1 = cv2.imread(path +'\\color.png')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread(path +'\\test.jpg')
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#default nfeatures=500
orb = cv2.ORB_create(nfeatures=1000)

#keypoints
kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

print(des1.shape)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

print(len(good))
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

imgKp1 = cv2.drawKeypoints(img1, kp1, None)
imgKp2 = cv2.drawKeypoints(img2, kp2, None)

#cv2.imshow('imgKp1', imgKp1)
#cv2.imshow('imgKp2', imgKp2)
cv2.imshow('img3', img3)

filename = 'checks.jpg'
cv2.imwrite(os.path.join(path , filename), img3)
cv2.waitKey(0)
