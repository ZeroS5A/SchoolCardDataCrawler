from django.urls import path
from . import views

# 子应用路由
urlpatterns = [
    path('', views.demo)
]
