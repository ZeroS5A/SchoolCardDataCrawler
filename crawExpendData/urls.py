from django.urls import path

from crawExpendData import views

urlpatterns = [
    path('selectUser/', views.selectUser),
    path('insertExpend/', views.insertExpend),
    path('getImageCode/', views.getImageCode),
    path('setStuData/', views.setStuData),
    path('stuLogin/', views.stuLogin),
    path('drawData/', views.drawData),
    path('test', views.redisTest)
]
