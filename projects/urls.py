# projects/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import ProjectListView, ProjectDetailView, like_entry

# app_name = "projects"

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_index'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path("search/", views.project_search, name="project_search"),

    # Categories and Tags
    path("category/<slug:slug>/", views.project_category, name="project_category"),
    path("category/<slug:category_slug>/tag/<slug:tag_slug>/", views.project_category_tag, name="project_category_tag"),

    # Likes
    path('like/<int:entry_id>/', like_entry, name='like_entry'),

    # Tags (standalone)
    path("tag/<slug:slug>/", views.project_tag, name="project_tag"),
    path("tag/", RedirectView.as_view(pattern_name="project_index", permanent=False)),
]
