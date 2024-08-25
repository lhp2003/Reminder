import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time
import winsound
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk  # 导入Pillow库用于图像处理

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder")
        self.root.attributes("-topmost", True)  # 确保窗口在最上层

        # 加载PNG图片
        self.original_image = Image.open("robot-8449206_1280-removebg-preview.png")
        self.original_width, self.original_height = self.original_image.size

        # 计算图像的新尺寸，保持比例
        window_width = 1500  # 使用窗口的实际宽度
        aspect_ratio = self.original_width / self.original_height
        target_width = int(window_width * 0.3)  # 图像宽度占窗口宽度的30%
        target_height = int(target_width / aspect_ratio)

        # 调整图像大小
        resized_image = self.original_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)

        # 创建Canvas以放置图片和文字
        self.canvas = tk.Canvas(root, width=1000, height=1000)
        self.canvas.pack(fill="both", expand=True)

        # 在左上角放置图片
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        # 在图片右侧添加文本
        text_x = target_width + 10  # 10像素间隔
        text_y = target_height // 2  # 垂直居中
        self.canvas.create_text(text_x, text_y, anchor="w", text="Remember to take breaks every 20 minutes.",
                                font=('Helvetica', 14), fill="black")

        # 创建Meter小部件（分钟）
        self.minute_meter = ttkb.Meter(
            bootstyle='info',
            master=root,
            metersize=150,
            padding=5,
            meterthickness=15,
            stripethickness=18,
            amounttotal=20,       # 总共20分钟
            subtext="minutes",
            textfont='-size 24 -weight bold',       # 设置主要文本的字体大小和样式
            subtextfont='-size 15 -weight normal',  # 设置子文本的字体大小和样式
            interactive=False,
        )

        # 创建Meter小部件（秒钟）
        self.second_meter = ttkb.Meter(
            bootstyle='info',
            master=root,
            metersize=150,
            padding=5,
            meterthickness=15,
            stripethickness=6,
            amounttotal=60,       # 总共60秒
            subtext="seconds",
            textfont='-size 24 -weight bold',
            subtextfont='-size 15 -weight normal',
            interactive=False,
        )

        # 直接将两个Meter放置在窗口中央，并排排列
        meter_spacing = 50  # 两个Meter之间的间距
        center_x = 1500 // 2  # 窗口宽度为1500

        self.canvas.create_window(center_x - meter_spacing - 110, 500, window=self.minute_meter)  # 左侧 Meter
        self.canvas.create_window(center_x + meter_spacing + 110, 500, window=self.second_meter)  # 右侧 Meter

        # 启动提醒线程
        self.reminder_thread = Thread(target=self.reminder_loop)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()

        # 启动计时线程
        self.timer_thread = Thread(target=self.timer_loop)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def reminder_loop(self):
        while True:
            time.sleep(1200)  # 每20分钟提醒一次
            self.show_reminder()

    def show_reminder(self):
        self.root.after(0, self.display_message)
        self.play_sound()

    def display_message(self):
        # 弹出提示窗口
        messagebox.showinfo("remind", "Time for a 20-second break.！")
        # 还原窗口显示
        self.root.deiconify()

    def play_sound(self):
        # 播放声音
        winsound.Beep(1000, 1000)  # 1000 Hz 的声音，持续 1 秒

    def timer_loop(self):
        while True:
            for remaining in range(1200, -1, -1):  # 1200秒 = 20分钟
                minutes, seconds = divmod(remaining, 60)
                self.update_meters(minutes, seconds)
                time.sleep(1)
            self.reset_timer()

    def update_meters(self, minutes, seconds):
        # 更新 Meter 的值
        self.root.after(0, self.minute_meter.amountusedvar.set, minutes)
        self.root.after(0, self.second_meter.amountusedvar.set, seconds)

    def reset_timer(self):
        # 重置计时器并显示提醒
        self.show_reminder()

if __name__ == "__main__":
    root = ttkb.Window(
        themename="flatly",
        size=(1500, 1000),
        resizable=(False, False),
    )
    app = ReminderApp(root)
    root.mainloop()
