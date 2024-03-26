import cv2 as cv
import tkinter as tk
from tkinter import Button, Label, Toplevel
import threading
import pygame
import time
from PIL import Image, ImageTk

# 初始化pygame音频
pygame.init()
pygame.mixer.init()

# 加载警告声音文件
warning_sound = pygame.mixer.Sound('/水哥Project/警报声.wav')

# 上次检测到人脸的时间
last_face_detected_time = None
delay_to_stop_warning = 0.5  # 延迟1秒停止警报声音

# 是否正在运行人脸识别
is_running = False

# 创建全局label变量
label = None


def face_detect_demo(img):
    global last_face_detected_time, label

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

    # 将OpenCV图像转换为PIL Image对象
    frame_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)

    # 将PIL Image对象转换为Tkinter PhotoImage对象
    photo = ImageTk.PhotoImage(image=image)

    # 更新标签上的图像
    label.config(image=photo)
    label.photo = photo


# 函数，用于开始摄像头识别
def start_camera():
    global is_running

    is_running = True
    cap = cv.VideoCapture(0)

    while is_running:
        flag, frame = cap.read()
        if not flag:
            break
        face_detect_demo(frame)
        if cv.waitKey(1) & 0xFF == ord('q'):  # 按键盘上的 'q' 键退出
            break

    # 在退出循环后停止声音
    warning_sound.stop()
    cap.release()
    cv.destroyAllWindows()


def exit_program():
    global is_running
    is_running = False
    root.quit()  # 退出Tkinter主循环


def show_camera_window():
    global camera_window, label

    camera_window = Toplevel(root)
    camera_window.title("摄像头窗口")

    # 创建标签用于显示图像
    label = Label(camera_window)
    label.pack()

    # 创建返回按钮
    return_button = Button(camera_window, text="返回主界面", command=close_camera_window)
    return_button.pack()

    # 启动摄像头
    threading.Thread(target=start_camera).start()


def close_camera_window():
    global camera_window
    if camera_window is not None:
        camera_window.destroy()


# 创建Tkinter主窗口
root = tk.Tk()
root.title("人脸识别程序")

# 创建按钮
start_button = Button(root, text="开始摄像头识别", command=show_camera_window)
start_button.pack()

exit_button = Button(root, text="退出程序", command=exit_program)
exit_button.pack()

# 初始化摄像头窗口
camera_window = None

# 启动Tkinter主循环
root.mainloop()
