import cv2 as cv


def face_detect_demo(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 将图像转换为灰度图像
    face_detect = cv.CascadeClassifier('D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_detect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 在识别到的人脸周围绘制矩形

    cv.imshow('result', img)


# 读取默认摄像头（通常为 0）
cap = cv.VideoCapture(0)

while True:
    flag, frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if cv.waitKey(1) & 0xFF == ord('q'):  # 按键盘上的 'q' 键退出
        break

cap.release()
cv.destroyAllWindows()
