import cv2 as cv

img = cv.imread ('face1.jpg')

cv.imshow ('read_img',img)

cv.waitKey(0)

cv.destroyAllWindows()