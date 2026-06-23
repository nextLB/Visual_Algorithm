from django.shortcuts import render
from django.http import HttpResponse

# 首页视图
def home(request):
    return HttpResponse("""
        <h1>🎨 视觉算法演示平台</h1>
        <p>欢迎来到图像与视频算法测试界面！</p>
        <p>后续将在这里集成图像分类、目标检测等功能。</p>
    """)
