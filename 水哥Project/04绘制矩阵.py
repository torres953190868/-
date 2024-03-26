import cv2 as cv

img = cv.imread ('face1.jpg')

#坐标
x,y,w,h = 100, 100, 100, 100

#绘制矩形       xy起始点坐标， 后两个是长和宽
cv.rectangle(img,(x,y,x+w,y+h),color=(0,0,255),thickness=1)

#绘制原型              原点坐标
cv.circle(img,center=(x+w,y+h),radius=100,color=(255,0,0),thickness=1)

cv.imshow('img',img)

#等待,如果检测到键盘输入q,则结束进程
while True:
    if ord('q') == cv.waitKey(0):
        break

cv.destroyAllWindows()