"""
    create on 2026.06.18
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys




READ_BASE_DATA_DIR_PATH = '/home/next/桌面/Open_Source_Dataset_For_Visual_Algorithms/Camvid/'

SAVE_BASE_DATA_DIR_PATH = '/home/next/桌面/Open_Source_Dataset_For_Visual_Algorithms/General_Visual_Algorithm_Dataset/'

TRAIN_DIR = 'train'
TRAIN_LABEL_DIR = 'train_labels'
TRAIN_MASK_DIR = 'trainMasks'









if __name__ == '__main__':

    print('开始运行脚本程序,有助于详细理解Camvid数据集')

    # 以训练数据集为例，进行加载与分析
    trainImagePath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_DIR)
    imageFiles = sorted(os.listdir(trainImagePath))

    # 逐张加载与展示图像与标签数据等
    for singleImageFile in imageFiles:
        baseName = os.path.splitext(singleImageFile)[0]
        singleLabelFile = baseName + "_L.png"
        singleMaskFile = baseName + "_L.png"
        singleImagePath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_DIR, singleImageFile)
        singleLabelPath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_LABEL_DIR, singleLabelFile)
        singleMaskPath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_MASK_DIR, singleMaskFile)

        # 读取原图  
        imageBGR = cv2.imread(singleImagePath)
        if imageBGR is None:
            sys.exit(f"无法读取: {singleImagePath}")
        imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
        print(imageRGB)

        # 读取彩色标签图    三通道彩色
        labelBGR = cv2.imread(singleLabelPath)
        
    


