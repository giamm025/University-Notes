import cv2
import numpy as np

# create the 2 images we'll use to work
img1 = np.zeros((300, 300), dtype='uint8')  # create a black image, 300x300 pixels, with 8 bit unsigned integer values (0-255)
img2 = np.zeros((300, 300), dtype='uint8')  # create a black image, 300x300 pixels, with 8 bit unsigned integer values (0-255)

# draw a square in img1
img1 = cv2.rectangle(img1, (50, 50), (150, 150), 255, -1)  # draw a white square in img1, from (50, 50) to (150, 150), with a thickness of -1 (which means that the square will be filled)

# draw a circle in img2
img2 = cv2.circle(img2, (150, 150), 70, 255, -1)  # draw a filled white circle in img2 with the center at (150, 150) and radius 70

# AND operator: the result will be the intersection of the two shapes
# The resulting image will have white pixels only where both img1 and img2 have white pixels. 
and_img = cv2.bitwise_and(img1, img2) 

# OR operator: the result will be the union of the two shapes
# The resulting image will have white pixels where either img1 or img2 (or both) have white pixels.
or_img = cv2.bitwise_or(img1, img2)

# XOR operator: the result will be the exclusive OR of the two shapes
# The resulting image will have white pixels where either img1 or img2 (but not both) have white pixels.
xor_img = cv2.bitwise_xor(img1, img2)

# NOT operator: the result will be the inverse of the image
# The resulting image will have white and black pixels inverted. 
not_img2 = cv2.bitwise_not(img2) 

# concatenate the three images horizontally, so that we can see them all together
concat1 = np.hstack((img1, img2, and_img))  
concat2 = np.hstack((or_img, xor_img, not_img2))
final = np.vstack((concat1, concat2)) 

# show the images
cv2.imshow("final", final)
cv2.waitKey(0)