from PIL import ImageGrab
from PIL import Image
import os
import time
import numpy as np
import pystray
import ctypes
import msvcrt
import threading
import win32api
import win32con
import winreg

def hide_window():
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        ctypes.windll.user32.ShowWindow(hWnd, 0)

def hw():
    while True:
        key = msvcrt.getch()
        if key == b'\x1b': 
            hide_window()
            
def find_genshin_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\miHoYo\原神")
        path, _ = winreg.QueryValueEx(key, "game_install_path")
        winreg.CloseKey(key)
        return path
    except FileNotFoundError:
        return None

def get_percent(low, high):
    width, height = ss_img.size
    data = np.array(ss_img)
    count = np.sum(np.all((data >= low) & (data <= high), axis=2))
    percentage = count / (width * height)
    return percentage

def get_now_time():
    end_time = time.time()
    return end_time - start_time

t = threading.Thread(target = hw)

start_time = time.time()

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
allow_f= int(config["allow_f"])

_flag = 0
if(allow_f == 1):
    g_path = find_genshin_path()
    if g_path is not None:
        genshin_path = g_path
    else:
        _flag = 1

#main
count = 0;
while(_flag != 1):
    time.sleep(sleep_second)#单位是秒
    count += 1
    current_dir = os.getcwd()
    ss_img = ImageGrab.grab()
    _time = get_now_time()
    if _time >= time_limit:
        break
    if get_percent([color_range1, color_range2, color_range3], [255, 255, 255]) >= threshold:
        os.system(f'"{genshin_path}"')
        time.sleep(opening_sleep_second)