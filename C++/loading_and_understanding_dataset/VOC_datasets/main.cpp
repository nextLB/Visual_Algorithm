// create on 2026.06.26


#include <iostream>
#include <string>
#include <vector>
#include <filesystem>
#include <algorithm>
#include <opencv2/opencv.hpp>
#include <tinyxml2.h>




using namespace std;
namespace fs = std::filesystem;
using namespace cv;






// VOC 2007 的 20 个类别名称
const vector<string> VOC_CLASSES = {
    "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow",
    "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
};



// 为每个类别分配固定颜色（BGR 格式）
vector<Scalar> getClassColors() {
    vector<Scalar> colors;
    RNG rng(12345);
    for (size_t i = 0; i < VOC_CLASSES.size(); ++i) {
        colors.push_back(Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255)));
    }
    return colors;
}






int main() {

    // 可视化模式的设置
    string mode = "detection";
    string baseDir = "/home/next/桌面/Open_Source_Dataset_For_Visual_Algorithms/VOC/";

    // VOC 2007
    string VOC2007ImageDir = baseDir + "VOC2007/VOC2007_train_and_val/JPEGImages/";
    string VOC2007AnnoDir = baseDir + "VOC2007/VOC2007_train_and_val/Annotations/";
    string VOC2007SegClassDir = baseDir + "VOC2007/VOC2007_train_and_val/SegmentationClass/";
    string VOC2007SegObjectDir = baseDir + "VOC2007/VOC2007_train_and_val/SegmentationObject/";

    // 获取图像列表
    vector<string> imageFiles;
    for (const auto& entry : fs::directory_iterator(VOC2007ImageDir)) {
        string ext = entry.path().extension().string();
        if (ext == ".jpg" || ext == ".jpeg" || ext == ".png")
            imageFiles.push_back(entry.path().filename().string());
    }

    sort(imageFiles.begin(), imageFiles.end());
    cout << "共找到" << imageFiles.size() << "张图像，模式" << mode << endl;
    // 简单输出一下所有图像的完整路径
    for (const auto& fname : imageFiles) {
        fs::path fullPath = fs::path(VOC2007ImageDir) / fname;  // 拼接目录与文件名
        cout << fullPath.string() << endl;
    }



    // 获取类别颜色
    vector<Scalar> colors = getClassColors();

    // 逐张读取图像数据，并可视化
    for (size_t i = 0; i < imageFiles.size(); ++i) {
        const string& fname = imageFiles[i];
        string base = fname.substr(0, fname.find_last_of('.'));
        string imagePath = VOC2007ImageDir + fname;
        string xmlPath = VOC2007AnnoDir + base + ".xml";

        Mat imageBGR = imread(imagePath);
        if (imageBGR.empty()) {
            cerr << "无法读取图像: " << imagePath << endl;
            continue;
        }

        Mat displayImg;
        string windowTitle = "VOC2007 - " + mode;

        cout << windowTitle << endl;

    }


    return 0;
}


