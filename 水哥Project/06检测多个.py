import cv2 as cv

def face_detect_demo():
    gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    face_detect = cv.CascadeClassifier('D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    face = face_detect.detectMultiScale(gray)
    for x,y,w,h in face:
        cv.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
    cv.imshow('result',img)

img = cv.imread ('face3.jpg')
#检测函数
face_detect_demo()

#等待,如果检测到键盘输入q,则结束进程
while True:
    if ord('q') == cv.waitKey(0):
        break

cv.destroyAllWindows()