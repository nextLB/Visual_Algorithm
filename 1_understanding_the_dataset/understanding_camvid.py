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



# -------------------  定义 CamVid 的颜色映射（将类别ID映射为RGB） -------------------
# 索引0~31对应各类别，这里列出官方颜色（部分常用类别，可根据需要补充）
ID_TO_COLOR = np.array([
    [0, 0, 0],          # 0: 未标注/背景
    [128, 0, 0],        # 1: Animal
    [0, 128, 0],        # 2: Archway
    [128, 128, 0],      # 3: Bicyclist
    [0, 0, 128],        # 4: Bridge
    [128, 0, 128],      # 5: Building
    [0, 128, 128],      # 6: Car
    [128, 128, 128],    # 7: CartLuggagePram
    [64, 0, 0],         # 8: Child
    [192, 0, 0],        # 9: Column_Pole
    [64, 128, 0],       # 10: Fence
    [192, 128, 0],      # 11: LaneMkgsDriv
    [64, 0, 128],       # 12: LaneMkgsNonDriv
    [192, 0, 128],      # 13: Misc_Text
    [64, 128, 128],     # 14: MotorcycleScooter
    [192, 128, 128],    # 15: OtherMoving
    [0, 64, 0],         # 16: ParkingBlock
    [128, 64, 0],       # 17: Pedestrian
    [0, 192, 0],        # 18: Road
    [128, 192, 0],      # 19: RoadShoulder
    [0, 64, 128],       # 20: Sidewalk
    [128, 64, 128],     # 21: SignSymbol
    [0, 192, 128],      # 22: Sky
    [128, 192, 128],    # 23: SUVPickupTruck
    [64, 64, 0],        # 24: TrafficCone
    [192, 64, 0],       # 25: TrafficLight
    [64, 192, 0],       # 26: Train
    [192, 192, 0],      # 27: Tree
    [64, 64, 128],      # 28: Truck_Bus
    [192, 64, 128],     # 29: Tunnel
    [64, 192, 128],     # 30: VegetationMisc
    [192, 192, 128],    # 31: Wall
], dtype=np.uint8)

CAMVID_CATEGORIES_N = 32





if __name__ == '__main__':

    print('开始运行脚本程序,有助于详细理解Camvid数据集')

    # 以训练数据集为例，进行加载与分析
    trainImagePath = os.path.join(READ_BASE_DATA_DIR_PATH, TRAIN_DIR)
    imageFiles = sorted(os.listdir(trainImagePath))
    print(imageFiles)
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
        print(f"imageRGB: {imageBGR}, imageRGB shape: {imageRGB.shape}")

        # 读取彩色标签图    三通道彩色
        labelBGR = cv2.imread(singleLabelPath)
        if labelBGR is None:
            sys.exit(f"无法读取彩色标签：{singleLabelPath}")
        labelRGB = cv2.cvtColor(labelBGR, cv2.COLOR_BGR2RGB)
        print(f"labelRGB: {labelRGB}, labelRGB shape: {labelRGB.shape}")
    
        # 读取单通道掩码 （trainMaks）  单通道灰度
        maskID = cv2.imread(singleMaskPath, cv2.IMREAD_GRAYSCALE)
        if maskID is None:
            sys.exit(f"无法读取掩码：{singleMaskPath}")
        print(f"maskID: {maskID}, maskID shape: {maskID.shape}")
        

        # 将单通道ID转换为彩色
        # 方法：利用颜色映射表，将每个像素的ID替换为对应的RGB值
        h, w = maskID.shape
        maskColor = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(CAMVID_CATEGORIES_N):
            maskColor[maskID == i] = ID_TO_COLOR[i]
        

        # 叠加图: 原图 + 彩色标签（半透明）
        overlay = cv2.addWeighted(imageRGB, 0.6, labelRGB, 0.4, 0)

        # 创建 2x2 子图布局
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'CamVid sample showcase: {singleImageFile}', fontsize=14)

        axes[0, 0].imshow(imageRGB)
        axes[0, 0].set_title('Original Image')
        axes[0, 0].axis('off')

        axes[0, 1].imshow(labelRGB)
        axes[0, 1].set_title('Color labels (train_labels)')
        axes[0, 1].axis('off')

        axes[1, 0].imshow(maskColor)  # 从单通道ID转换的伪彩色
        axes[1, 0].set_title('Single-channel mask (trainMasks) pseudocolor')
        axes[1, 0].axis('off')

        axes[1, 1].imshow(overlay)
        axes[1, 1].set_title('Original image with colored labels overlay')
        axes[1, 1].axis('off')

        plt.tight_layout()
        plt.show()

