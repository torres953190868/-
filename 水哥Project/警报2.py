import cv2 as cv
import pygame
import time

# 初始化pygame音频
pygame.init()
pygame.mixer.init()

# 加载警告声音文件
warning_sound = pygame.mixer.Sound('/水哥Project/警报声.wav')

# 上次检测到人脸的时间
last_face_detected_time = None
delay_to_stop_warning = 1  # 延迟1秒停止警报声音


def face_detect_demo(img):
    global last_face_detected_time

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 将图像转换为灰度图像
    face_detect = cv.CascadeClassifier('D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_detect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        # 如果没有检测到人脸，检查上次检测到人脸的时间
        if last_face_detected_time is not None and time.time() - last_face_detected_time >= delay_to_stop_warning:
            warning_sound.stop()
    else:
        # 如果检测到人脸，记录当前时间
        last_face_detected_time = time.time()
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 在识别到的人脸周围绘制矩形
            # 播放警告声音，如果已经在播放，将不会重新播放
            if pygame.mixer.get_busy() == 0:
                warning_sound.play()

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

# 在退出循环后停止声音
warning_sound.stop()
cap.release()
cv.destroyAllWindows()  # 关闭窗口



