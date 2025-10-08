from django.urls import path
from django.views.generic import RedirectView
from . import views
from .views import like_entry, PostListView, PostDetailView, ProjectListView, ProjectDetailView, TutorialListView, TutorialDetailView

urlpatterns = [
    # path("search/", views.project_search, name="project_search"),

    # Posts
    # path('posts/', PostListView.as_view(), name='post_index'),
    # path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

    # Projects
    # path('projects/', ProjectListView.as_view(), name='project_index'),
    # path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),

    # Tutorials
    # path('tutorials/', TutorialListView.as_view(), name='tutorial_index'),
    # path('tutorials/<slug:slug>/', TutorialDetailView.as_view(), name='tutorial_detail'),

    # Categories and Tags
    # path("category/<slug:slug>/", views.project_category, name="project_category"),
    # path("category/<slug:category_slug>/tag/<slug:tag_slug>/", views.project_category_tag, name="project_category_tag"),

    # # Likes
    path('like/<int:entry_id>/', like_entry, name='like_entry'),

    # # Tags (standalone)
    # path("tag/<slug:slug>/", views.project_tag, name="project_tag"),
    # path("tag/", RedirectView.as_view(pattern_name="project_index", permanent=False)),
]



#   path("", views.project_index, name="project_index"),
#     path("search/", views.project_search, name="project_search"),
#     path('featured/', views.featured_projects, name='featured_projects'),
#     path("project/<slug:slug>/", views.project_detail, name="project_detail"),
#     path("project/", RedirectView.as_view(pattern_name="project_index", permanent=False)),
#     # Categories 
#     path("category/<slug:slug>/", views.project_category, name="project_category"),
#     # path('category/<slug:category_slug>/tag/<slug:tag_slug>/', views.projects_by_category_and_tag, name='projects_by_category_and_tag'),
#     path("category/", RedirectView.as_view(pattern_name="project_index", permanent=False)),
#     # Tags
#     path("tag/<slug:slug>/", views.project_tag, name="project_tag"),
#     path("tag/", RedirectView.as_view(pattern_name="project_index", permanent=False)),

#     path('<slug:slug>/like/', views.project_like, name='project_like'),  # <- use the AJAX one
#     path('<slug:slug>/comment/', views.project_comment, name='project_comment'),
#     path('<slug:slug>/comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),