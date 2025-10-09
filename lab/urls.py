# lab/urls.py
from django.urls import path
from . import views

# app_name = "lab"

urlpatterns = [
    path('', views.lab_view, name='lab'),
    # path('', views.lab_list, name='lab_list'),
    # path('<int:pk>/', views.lab_detail, name='lab_detail'),
]
