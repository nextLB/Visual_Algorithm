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
CLASSES = ["crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"]



def extract_number(filename):
    match = re.search(r'_(\d+)\.', filename)
    return int(match.group(1)) if match else 0







# 绘制边界框
def draw_boxes_on_image(imageBGR, labelPath):

    image = imageBGR.copy()

    h, w, _ = image.shape
    if not os.path.exists(labelPath):
        return image

    with open(singleLabelPath, 'r') as f:
        lines = f.readlines()


    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue

        clsID, x_c, y_c, bw_norm, bh_norm = map(float, parts)
        clsID = int(clsID)
        # 转换为像素坐标
        x = (x_c - bw_norm/2) * w
        y = (y_c - bh_norm/2) * h
        bw = bw_norm * w
        bh = bh_norm * h
        x1, y1, x2, y2 = int(x), int(y), int(x+bw), int(y+bh)
        # 绘制矩形（绿色）
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 类别标签
        label = CLASSES[clsID] if clsID < len(CLASSES) else f"class{clsID}"
        cv2.putText(image, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image



if __name__ == '__main__':
    print('开始运行脚本程序,有助于详细理解NEY_YOLO数据集')


    # 以训练数据集为例，进行加载与分析
    trainImagePath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_DIR, IMAGE_DIR)
    imageFiles = sorted(os.listdir(trainImagePath), key=extract_number)
    print(imageFiles)

    idx = 0
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
        imageWithBoxesBGR = draw_boxes_on_image(imageBGR, singleLabelPath)

        # 转换为BGR 供 matplotlib 显示
        imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
        imageWithBoxesRGB = cv2.cvtColor(imageWithBoxesBGR, cv2.COLOR_BGR2RGB)


        # ---- 创建子图展示 ----
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle(f'NEU-YOLO Sample: {singleImageFile} (No.{idx + 1}/{len(imageFiles)})', fontsize=14)

        # 左：原始图像
        axes[0].imshow(imageRGB)
        axes[0].set_title('Original Image')
        axes[0].axis('off')

        # 右：带边界框的图像
        axes[1].imshow(imageWithBoxesRGB)
        axes[1].set_title('With Bounding Boxes')
        axes[1].axis('off')

        plt.tight_layout()
        plt.show()  # 非阻塞显示

        idx += 1

    print("可视化结束。")

