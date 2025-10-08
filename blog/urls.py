# blog/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import PostListView, PostDetailView, like_entry

# app_name = "blog"

urlpatterns = [
    path('', PostListView.as_view(), name='post_index'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path("search/", views.post_search, name="post_search"),

    # Categories and Tags
    path("category/<slug:slug>/", views.post_category, name="post_category"),
    path("category/<slug:category_slug>/tag/<slug:tag_slug>/", views.post_category_tag, name="post_category_tag"),

    # Likes
    path('like/<int:entry_id>/', like_entry, name='like_entry'),

    # Tags (standalone)
    path("tag/<slug:slug>/", views.post_tag, name="post_tag"),
    path("tag/", RedirectView.as_view(pattern_name="post_index", permanent=False)),
]
