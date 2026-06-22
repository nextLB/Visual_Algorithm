"""
    create on 2026.06.22
"""


import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys



READ_BASE_DATA_DIR_PATH = '/home/next/桌面/Open_Source_Dataset_For_Visual_Algorithms/NEU_YOLO/'

SAVE_BASE_DATA_DIR_PATH = '/home/next/桌面/Open_Source_Dataset_For_Visual_Algorithms/General_Visual_Algorithm_Dataset/'

TRAIN_DIR = 'train/train'
VALID_DIR = 'valid/valid'

IMAGE_DIR = 'images'
LABEL_DIR = 'labels'


# 关于这个缺陷检测数据集的缺陷类别
# crazing   裂纹
# inclusion     夹杂物
# patches   斑块
# pitted_surface    麻面
# rolled-in_scale   氧化皮压入
# scratches 划痕
classes = ["crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"]



def extract_number(filename):
    match = re.search(r'_(\d+)\.', filename)
    return int(match.group(1)) if match else 0







# 绘制边界框
def draw_boxes_on_image(imageBGR, labelPath):

    pass






if __name__ == '__main__':
    print('开始运行脚本程序,有助于详细理解NEY_YOLO数据集')


    # 以训练数据集为例，进行加载与分析
    trainImagePath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_DIR, IMAGE_DIR)
    imageFiles = sorted(os.listdir(trainImagePath), key=extract_number)
    print(imageFiles)

    # 逐张加载与展示图像与标签数据等
    for singleImageFile in imageFiles:
        baseName = os.path.splitext(singleImageFile)[0]
        singleLabelFile = baseName + ".txt"
        singleImagePath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_DIR, IMAGE_DIR, singleImageFile)
        singleLabelPath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_DIR, LABEL_DIR, singleLabelFile)

        # 读取图像数据  (BGR)
        imageBGR = cv2.imread(singleImagePath)
        if imageBGR is None:
            sys.exit(f"无法读取: {singleImagePath}")
        
        # 绘制边界框



