# projects/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import ProjectListView, ProjectDetailView

# app_name = "projects"

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_index'),
    path("search/", views.project_search, name="project_search"),
    path("tag/<slug:slug>/", views.project_tag, name="project_tag"),
    path("tag/", RedirectView.as_view(pattern_name="project_index", permanent=False)),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]
