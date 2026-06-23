from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 空路径指向 home 视图
]
