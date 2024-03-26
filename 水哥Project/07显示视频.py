import cv2 as cv

def face_detect_demo():
    gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    face_detect = cv.CascadeClassifier('D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    face = face_detect.detectMultiScale(gray)
    for x,y,w,h in face:
        cv.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
    cv.imshow('result',img)

#读取摄像头
cap = cv.VideoCapture(700)

#等待,如果检测到键盘输入q,则结束进程
while True:
    flag,frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if ord('q') == cv.waitKey(1):
        break

cv.destroyAllWindows()