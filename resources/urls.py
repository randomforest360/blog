from django.urls import path
from . import views

app_name = "resources"

urlpatterns = [
    path("", views.ResourceListView.as_view(), name="index"),
    path("<int:pk>/", views.ResourceDetailView.as_view(), name="detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
]
