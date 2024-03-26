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
warning_sound = pygame.mixer.Sound('警报声.wav')

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

# 创建Tkinter主窗口
root = tk.Tk()
root.title("人脸识别与二维码识别程序")
root.geometry("400x300")  # 设置主窗口大小

# 标签用于显示图像
label = Label(root)
label.pack(pady=10)  # 增加垂直间距

# 按钮样式
button_style = {"font": ("Helvetica", 14), "width": 20, "height": 2}

# 创建按钮
start_button = Button(root, text="开始摄像头识别", command=show_camera_window, **button_style)
start_button.pack()

qr_code_button = Button(root, text="识别二维码", command=show_qr_code_window, **button_style)
qr_code_button.pack()

exit_button = Button(root, text="退出程序", command=exit_program, **button_style)
exit_button.pack()

# 初始化摄像头窗口和二维码窗口
camera_window = None
qr_code_window = None
camera_thread = None

# 启动Tkinter主循环
root.mainloop()
