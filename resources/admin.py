from django.contrib import admin
from .models import ResourceCategory, Resource

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'tags')
    ordering = ('-created_at',)
