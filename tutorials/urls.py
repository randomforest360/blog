# # tutorials/urls.py
# from django.urls import path
# from . import views

# # app_name = "tutorials"

# urlpatterns = [
#     # path('', views.tutorial_list, name='tutorial_list'),
#     # path('<int:pk>/', views.tutorial_detail, name='tutorial_detail'),
# ]
# tutorials/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import TutorialListView, TutorialDetailView, like_entry

# app_name = "tutorials"

urlpatterns = [
    path('', TutorialListView.as_view(), name='tutorial_index'),
    path('<slug:slug>/', TutorialDetailView.as_view(), name='tutorial_detail'),
    path("search/", views.tutorial_search, name="tutorial_search"),

    # Categories and Tags
    path("category/<slug:slug>/", views.tutorial_category, name="tutorial_category"),
    path("category/<slug:category_slug>/tag/<slug:tag_slug>/", views.tutorial_category_tag, name="tutorial_category_tag"),

    # Likes
    path('like/<int:entry_id>/', like_entry, name='like_entry'),

    # Tags (standalone)
    path("tag/<slug:slug>/", views.tutorial_tag, name="tutorial_tag"),
    path("tag/", RedirectView.as_view(pattern_name="tutorial_index", permanent=False)),
]
