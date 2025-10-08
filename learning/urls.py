# learning/urls.py
from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    path('', views.path_list, name='path_list'),
    path('<slug:slug>/', views.path_detail, name='path_detail'),
    path('<slug:path_slug>/lesson/<int:order>/', views.lesson_detail, name='lesson_detail'),
]
