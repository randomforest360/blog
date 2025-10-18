"""
URL configuration for devlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('projects/', include('projects.urls')),
    path('blog/', include('blog.urls')),
    path('lab/', include('lab.urls')),
    path('learning-paths/', include('learning.urls')),
    path('resources/', include('resources.urls')),
    path('glossary/', include('glossary.urls')),
 
    
    # path('gallery/', include('gallery.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# reate a “Trending” View or Section
# You can build a view that shows:

# Most liked entries in the past week

# Most liked tutorials vs projects

# Recently published entries with high engagement