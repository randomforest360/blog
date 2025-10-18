# blog/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import PostListView, PostDetailView

# app_name = "blog"

urlpatterns = [
    path('', PostListView.as_view(), name='post_index'),
    path("search/", views.post_search, name="post_search"),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

    # Tags
    path("tag/<slug:slug>/", views.post_tag, name="post_tag"),
    path("tag/", RedirectView.as_view(pattern_name="post_index", permanent=False)),
]
