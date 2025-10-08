# core/admin.py
from django.contrib import admin
from .models import SocialLink

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "is_visible")
    list_filter = ("platform", "is_visible")
    search_fields = ("platform", "url")
