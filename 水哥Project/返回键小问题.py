import cv2 as cv
import tkinter as tk
from tkinter import Button, Label, Toplevel, messagebox
import threading
import pygame
import time
from PIL import Image, ImageTk
import qrcode

# 初始化pygame音频
pygame.init()
pygame.mixer.init()

# 加载警告声音文件
warning_sound = pygame.mixer.Sound('/水哥Project/警报声.wav')

# 上次检测到人脸的时间
last_face_detected_time = None
delay_to_stop_warning = 1  # 延迟1秒停止警报声音

# 是否正在运行人脸识别
is_running_face_detection = False

# 创建全局label变量
label = None

# 创建全局变量，用于存储二维码内容
qr_code_content = None

# 创建全局变量，用于存储摄像头线程
camera_thread = None

# 在全局创建一个标志，用于控制循环是否继续运行
is_running = True

def face_detect_demo(img):
    global last_face_detected_time, label

    if is_running_face_detection:  # 只有在启用人脸识别功能时才执行以下代码
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 将图像转换为灰度图像
        face_detect = cv.CascadeClassifier(
            'D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
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
    global is_running_face_detection, is_running, camera_thread

    is_running_face_detection = True  # 启用人脸识别功能
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
    is_running_face_detection = False  # 禁用人脸识别功能


# 函数，用于同时进行摄像头捕获和二维码识别
def capture_and_recognize():
    global label, qr_code_content, camera_thread, is_running

    cap = cv.VideoCapture(0)

    while True:
        flag, frame = cap.read()
        if not flag:
            break

        # 识别二维码
        detector = cv.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(frame)

        if retval:
            qr_code_content = decoded_info[0]
            break

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # 将OpenCV图像转换为PIL Image对象
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # 将PIL Image对象转换为Tkinter PhotoImage对象
        photo = ImageTk.PhotoImage(image=image)

        # 更新标签上的图像
        label.config(image=photo)
        label.photo = photo

    cap.release()
    cv.destroyAllWindows()

    # 在识别完成后更新label的内容
    if label is not None:
        label.config(text=f"二维码内容：{qr_code_content}")

    is_running = False  # 设置标志以退出循环


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


# 函数，用于关闭摄像头窗口和停止警报声音
def close_camera_window():
    global camera_window

    # 渐渐降低声音的音量并停止音频播放
    warning_sound.fadeout(500)  # 500毫秒内渐渐降低音量到0，然后停止

    # 等待一段时间，确保声音已经停止
    time.sleep(0.5)  # 可以根据需要调整等待的时间

    if camera_window is not None:
        camera_window.destroy()
        camera_window = None





# 函数，用于识别二维码
def recognize_qr_code():
    global qr_code_content, label
    cap = cv.VideoCapture(0)

    while True:
        flag, frame = cap.read()
        if not flag:
            break

        # 识别二维码
        detector = cv.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(frame)

        if retval:
            qr_code_content = decoded_info[0]
            break

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    # 在识别完成后更新label的内容
    if label is not None:
        label.config(text=f"二维码内容：{qr_code_content}")


# 函数，用于显示二维码窗口
def show_qr_code_window():
    global qr_code_window, qr_code_content, camera_thread, label

    # 初始化qr_code_content
    qr_code_content = None

    # 创建一个新的线程来捕获摄像头并进行二维码识别
    camera_thread = threading.Thread(target=capture_and_recognize)
    camera_thread.start()

    qr_code_window = Toplevel(root)
    qr_code_window.title("二维码识别窗口")

    label = Label(qr_code_window, text="正在识别二维码...")
    label.pack()

    return_button = Button(qr_code_window, text="返回主界面", command=close_qr_code_window)
    return_button.pack()


# 函数，用于关闭二维码识别窗口
def close_qr_code_window():
    global qr_code_window

    if qr_code_window is not None:
        qr_code_window.destroy()
        qr_code_window = None



# 创建Tkinter主窗口
root = tk.Tk()
root.title("人脸识别与二维码识别程序")

# 创建按钮
start_button = Button(root, text="开始摄像头识别", command=show_camera_window)
start_button.pack()

qr_code_button = Button(root, text="识别二维码", command=show_qr_code_window)
qr_code_button.pack()

exit_button = Button(root, text="退出程序", command=exit_program)
exit_button.pack()

# 初始化摄像头窗口和二维码窗口
camera_window = None
qr_code_window = None
camera_thread = None

# 启动Tkinter主循环
root.mainloop()