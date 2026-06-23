# 视觉算法 (Give me a picture or a video, and I’ll tell you what it is.)


## understanding_the_dataset

    understading_camvid.py      理解与熟悉camvid数据集

> CamVid (Cambridge-driving Labeled Video Database，剑桥驾驶标注视频数据库) 是计算机视觉领域，
> 特别是自动驾驶场景理解方向的一个经典基准数据集。它由剑桥大学的研究团队于2008年左右发布，是首个包含逐像
> 素语义标签的视频数据集。
> CamVid 的数据采集方式与多数场景数据集不同，它不是来自固定位置的监控摄像头，而是从行驶中的汽车视角拍摄，
> 这使得数据更贴近真实的自动驾驶场景。数据集提供了超过10分钟的高质量30Hz视频footage,并从中提取了701张经
> 手动标注的图像。这些标签经过了严格的质检流程    ------  先由一人手动标注，再由第二人核查确认，保证了
> 标注的高质量。

    understanding_NEU_YOLO.py   理解与熟悉NEU YOLO数据集

> NEU-DET 是由东北大学发布并维护的，专为智能制造领域中金属表面质量检测算法的研究与优化而构建的基准数据集。
> 它专注于热轧钢带表面，包含了6种最常见的典型表面缺陷。由于缺陷样本规模相对较小（共1800张），它常被用作典
> 型的小样本工业场景数据集，用于验证算法在数据有限情况下的性能。


## picture_video_what_it_is
    
网站搭建与开发

简介如下

    python version: 3.11.15
    django version: 5.2.14
    在visual_algorithm_website文件夹下有文件夹如下
    visual_algorithm_website这个是根应用文件夹，是使用django-admin startproject visual_algorithm_website .这个命令创建出来的
    main_interface这个是具体应用的一个文件夹，是使用python ./manage.py startapp main_interface 这个命令创建出来的




核心算法研究与实验




