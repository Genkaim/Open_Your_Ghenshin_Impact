from ctypes import *
from PIL import ImageGrab
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
import os
import time
import numpy as np
import pystray
import time
import sys
import ctypes
import msvcrt
import threading
import subprocess

def hide_window():
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        ctypes.windll.user32.ShowWindow(hWnd, 0)

def hw():
    while True:
        key = msvcrt.getch()
        if key == b'\x1b': 
            hide_window()

t = threading.Thread(target = hw)


print("开始运行了喵🥳", end = "\n\n")
print("*因为time.sleep()函数放置位置和多线程的原因, 运行时间和Done的比值不一定为判断间隔🥲  建议判断间隔设置的比预期的小", end = "\n\n")
start_time = time.time()
def get_percent(img_path, low, high):
    im = Image.open(img_path)
    width, height = im.size
    data = np.array(im)
    count = np.sum(np.all((data >= low) & (data <= high), axis=2))
    percentage = count / (width * height)
    return percentage

def get_now_time():
    end_time = time.time()
    return end_time - start_time

config = {}
config_path = os.getcwd() + "\config.txt"
with open(config_path, 'r', encoding='utf-8') as f:
    for line in f:
        if not line.startswith('#'):
            key, value = line.split('=')
            config[key.strip()] = value.strip()

sleep_second = float(config["sleep_second"])
time_limit = float(config["time_limit"])
threshold = float(config["threshold"])
genshin_path = config["genshin_path"]
opening_sleep_second = int(config["opening_sleep_second"])
color_range1 = int(config["color_range1"])
color_range2 = int(config["color_range2"])
color_range3 = int(config["color_range3"])
_exit = int(config["_exit"])
allow_hide= int(config["allow_hide"])

if(allow_hide == 1):
    t.start()
    print("按ESC隐藏窗口", end = "\n\n")

#main
count = 0;
while(1):
    time.sleep(sleep_second)#单位是秒
    count += 1
    current_dir = os.getcwd()
    img_path = os.path.join(current_dir, 'display.png')
    if os.path.exists(img_path):
        os.remove(img_path)
    ss_img = ImageGrab.grab()
    ss_img.save(img_path)
    _time = get_now_time()
    if _time >= time_limit:
        break
    if get_percent(img_path, [color_range1, color_range2, color_range3], [255, 255, 255]) >= threshold:
        os.system(f'"{genshin_path}"')
        time.sleep(opening_sleep_second)
    print(f"\rDone: {count}    运行时间(s): {int(_time)}", end="")

if(_exit == 1):
    print("\n")
    print("=======================================================================\n")
    input("Press Enter to exit")
