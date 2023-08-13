# -*- coding: utf-8 -*-
from ctypes import *
from PIL import ImageGrab
from PIL import Image
import os
import time
import numpy as np
print("开始运行了喵🥳")
def get_percent(img_path, low, high):
    im = Image.open(img_path)
    width, height = im.size
    data = np.array(im)
    count = np.sum(np.all((data >= low) & (data <= high), axis=2))
    percentage = count / (width * height)
    return percentage

config = {}
config_path = os.getcwd() + "\config.txt"
with open(config_path, 'r', encoding='utf-8') as f:
    for line in f:
        if not line.startswith('#'):
            key, value = line.split('=')
            config[key.strip()] = value.strip()

sleep_second = float(config["sleep_second"])
get_count = int(config["get_count"])
threshold = float(config["threshold"])
genshin_path = config["genshin_path"]
opening_sleep_second = config["opening_sleep_second"]
color_range = int(config["color_range"])

for i in range(get_count):
    time.sleep(sleep_second)#单位是秒
    current_dir = os.getcwd()
    img_path = os.path.join(current_dir, 'display.png')
    if os.path.exists(img_path):
        os.remove(img_path)
    ss_img = ImageGrab.grab()
    ss_img.save(img_path)
    if get_percent(img_path, [color_range, color_range, color_range], [255, 255, 255]) >= threshold:
        os.system(f'"{genshin_path}"')
        time.sleep(opening_sleep_second)