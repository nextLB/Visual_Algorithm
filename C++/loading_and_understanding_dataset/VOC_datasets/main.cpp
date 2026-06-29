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

// 解析 XML 文件，返回所有目标的 (类别名, xmin, ymin, xmax, ymax)
vector<tuple<string, int, int, int, int>> parseVOCXML(const string& xmlPath) {
    vector<tuple<string, int, int, int, int>> objects;
    tinyxml2::XMLDocument doc;
    if (doc.LoadFile(xmlPath.c_str()) != tinyxml2::XML_SUCCESS) {
        cerr << "无法解析 XML: " << xmlPath << endl;
        return objects;
    }

    tinyxml2::XMLElement* root = doc.FirstChildElement("annotation");
    if (!root) return objects;

    tinyxml2::XMLElement* objElem = root->FirstChildElement("object");
    while (objElem) {
        string name;
        int xmin = 0, ymin = 0, xmax = 0, ymax = 0;

        tinyxml2::XMLElement* nameElem = objElem->FirstChildElement("name");
        if (nameElem) name = nameElem->GetText();

        tinyxml2::XMLElement* bndbox = objElem->FirstChildElement("bndbox");
        if (bndbox) {
            bndbox->FirstChildElement("xmin")->QueryIntText(&xmin);
            bndbox->FirstChildElement("ymin")->QueryIntText(&ymin);
            bndbox->FirstChildElement("xmax")->QueryIntText(&xmax);
            bndbox->FirstChildElement("ymax")->QueryIntText(&ymax);
        }

        objects.emplace_back(name, xmin, ymin, xmax, ymax);
        objElem = objElem->NextSiblingElement("object");
    }
    return objects;
}

// 绘制检测框（同之前）
Mat drawDetection(const Mat& imageBGR, const vector<tuple<string, int, int, int, int>>& objects,
                  const vector<Scalar>& colors) {
    Mat img = imageBGR.clone();
    for (const auto& obj : objects) {
        string name = get<0>(obj);
        int xmin = get<1>(obj), ymin = get<2>(obj);
        int xmax = get<3>(obj), ymax = get<4>(obj);

        int idx = -1;
        for (size_t i = 0; i < VOC_CLASSES.size(); ++i) {
            if (VOC_CLASSES[i] == name) { idx = i; break; }
        }
        Scalar color = (idx >= 0) ? colors[idx] : Scalar(0, 255, 0);

        rectangle(img, Point(xmin, ymin), Point(xmax, ymax), color, 2);
        string label = name;
        int baseLine = 0;
        Size labelSize = getTextSize(label, FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
        rectangle(img, Point(xmin, ymin - labelSize.height - baseLine),
                  Point(xmin + labelSize.width, ymin), color, FILLED);
        putText(img, label, Point(xmin, ymin - baseLine),
                FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 255, 255), 1);
    }
    return img;
}

// 读取分割掩码并生成叠加图（半透明）
Mat overlaySegmentation(const Mat& imageBGR, const Mat& segMask, double alpha = 0.4) {
    Mat maskBGR = segMask;
    if (maskBGR.size() != imageBGR.size()) {
        resize(maskBGR, maskBGR, imageBGR.size());
    }
    Mat overlay;
    addWeighted(imageBGR, 1 - alpha, maskBGR, alpha, 0, overlay);
    return overlay;
}






int main() {

    // 可视化模式的设置
    // string mode = "detection";
    string mode = "semantic";
    // string mode = "instance";
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


        // 目标检测
        if (mode == "detection") {
            auto objects = parseVOCXML(xmlPath);
            Mat imgWithBoxes = drawDetection(imageBGR, objects, colors);
            hconcat(imageBGR, imgWithBoxes, displayImg);   // 直接拼接两张 BGR 图像
        }
        // 语义分割
        else if (mode == "semantic") {
            string segPath = VOC2007SegClassDir + base + ".png";
            Mat segMask = imread(segPath, IMREAD_COLOR); // 自动应用调色板
            if (segMask.empty()) {
                cerr << "无法读取语义分割图(或是数据集中无该掩码图): " << segPath << endl;
                displayImg = imageBGR.clone();
                continue;
            } 
            else {
                if (segMask.size() != imageBGR.size())
                    resize(segMask, segMask, imageBGR.size());
                Mat overlay = overlaySegmentation(imageBGR, segMask, 0.4);
                hconcat(imageBGR, overlay, displayImg);
            }
        }
        // 实例分割
        else if (mode == "instance") {
            string segPath = VOC2007SegObjectDir + base + ".png";
            Mat segMask = imread(segPath, IMREAD_COLOR); // 自动应用调色板
            if (segMask.empty()) {
                cerr << "无法读取实例分割图(或是数据集中无该掩码图): " << segPath << endl;
                displayImg = imageBGR.clone();
                continue;
            } 
            else {
                if (segMask.size() != imageBGR.size())
                    resize(segMask, segMask, imageBGR.size());
                Mat overlay = overlaySegmentation(imageBGR, segMask, 0.4);
                hconcat(imageBGR, overlay, displayImg);
            }
        }



        // 添加图像编号
        string info = "[" + to_string(i+1) + "/" + to_string(imageFiles.size()) + "] " + fname;
        putText(displayImg, info, Point(10, 30), FONT_HERSHEY_SIMPLEX, 0.7, Scalar(0, 0, 255), 2);

        imshow(windowTitle, displayImg);
        int key = waitKey(0);
        if (key == 27) break;



    }


    return 0;
}


