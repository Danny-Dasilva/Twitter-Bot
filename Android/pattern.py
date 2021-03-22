import cv2
import numpy as np

img = cv2.imread('full.png')
# img = cv2.imread('pattern.png')
thresh = cv2.inRange(img, (116,116,116), (155,155,155))
print(thresh)
# thresh = cv2.bitwise_not(thresh)
contours, hiearchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cn = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 2000:
        print(area)
        cn.append(contour)
# print(len(contours))
    # print(area)
# mask = np.zeros(image.shape, dtype=np.uint8)
# print(contours, cn)
cv2.drawContours(img, cn, -1, (0,255,0), 3)
cv2.imshow('image', img)
cv2.imwrite('image.png', img)
cv2.waitKey(0)

