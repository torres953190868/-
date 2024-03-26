import qrcode

# 要加密为二维码的文本信息
text_to_encrypt = "姓名：李炜畅\n电话：110\n工号：1129912\n机房号码：1\n机器号码：2"

# 创建QRCode对象
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# 将文本信息添加到QRCode对象中
qr.add_data(text_to_encrypt)
qr.make(fit=True)

# 创建一个PIL图像对象
img = qr.make_image(fill_color="black", back_color="white")

# 保存二维码图像
img.save("my_qrcode.png")

# 显示二维码图像
img.show()
