import cv2 as cv

img = cv.imread ('face1.jpg')

#修改尺寸
resize_img = cv.resize(img, dsize=(200,200))

cv.imshow('img',img)

cv.imshow('resize_img',resize_img)

print('未修改：', img.shape)

print('修改后：',resize_img.shape)

#等待,如果检测到键盘输入q,则结束进程
while True:
    if ord('q') == cv.waitKey(0):
        break

cv.destroyAllWindows()