import  cv2
import numpy as np

sift = cv2.SIFT(10)

img1 = cv2.imread('laptop.jpg');
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
kp1, desc1 = sift.detectAndCompute(gray1, None)

img2 = cv2.imread('notebook.png');
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
kp2, desc2 = sift.detectAndCompute(gray2, None)

img3 = cv2.imread('pencil.jpg');
gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
kp3, desc3 = sift.detectAndCompute(gray3, None)

img4 = cv2.imread('printer.jpg');
gray4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
kp4, desc4 = sift.detectAndCompute(gray4, None)

np.savez_compressed('descriptors.npz', laptop=desc1, notebook=desc2, pencil=desc3, printer=desc4)



#print "Descriptors shape", desc.shape

#img = cv2.drawKeypoints(gray, kp)

#cv2.imwrite('sift_keypoints.jpg', img)
