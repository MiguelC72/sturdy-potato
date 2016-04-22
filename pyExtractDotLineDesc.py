import  cv2
import numpy as np

sift = cv2.SIFT()

img1 = cv2.imread('dot1.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
kp1, desc1 = sift.detectAndCompute(gray1, None)

img2 = cv2.imread('line2.png')
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
kp2, desc2 = sift.detectAndCompute(gray2, None)

'''
img3 = cv2.imread('pencil.jpg');
gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
kp3, desc3 = sift.detectAndCompute(gray3, None)

img4 = cv2.imread('printer.jpg');
gray4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
kp4, desc4 = sift.detectAndCompute(gray4, None)
'''
np.savez_compressed('dotLineDescriptors.npz', dot=desc1, line=desc2)



print "Descriptors 1 shape", desc1.shape
print "Descriptors 2 shape", desc2.shape

dot = cv2.drawKeypoints(gray1, kp1)
line = cv2.drawKeypoints(gray2, kp2)

cv2.imwrite('dot_keypoints.jpg', dot)
cv2.imwrite('line_keypoints.jpg', line)
