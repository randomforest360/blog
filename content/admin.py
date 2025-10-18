# from django.contrib import admin
# from .models import EntryCategory, EntryTag, Entry, EntryLink


# @admin.register(EntryCategory)
# class EntryCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "order", "slug")
#     prepopulated_fields = {"slug": ("name",)}
#     ordering = ("order",)


# @admin.register(EntryTag)
# class EntryTagAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug")
#     prepopulated_fields = {"slug": ("name",)}


# class EntryLinkInline(admin.TabularInline):
#     model = EntryLink
#     extra = 1


# @admin.register(Entry)
# class EntryAdmin(admin.ModelAdmin):
#     list_display = ("title", "type", "status", "author", "is_featured", "created_at", "updated_at")
#     list_filter = ("status", "type", "categories", "tags", "is_featured", "difficulty", "created_at")
#     search_fields = ("title", "excerpt", "body")
#     prepopulated_fields = {"slug": ("title",)}
#     inlines = [EntryLinkInline]
#     filter_horizontal = ("categories", "tags")
#     readonly_fields = ("reading_time", "likes_count", "created_at", "updated_at")
#     date_hierarchy = "created_at"


# @admin.register(EntryLink)
# class EntryLinkAdmin(admin.ModelAdmin):
#     list_display = ("title", "entry", "link_type", "url")
#     list_filter = ("link_type", "entry")
#     search_fields = ("title", "url")
# from django.contrib import admin
# from .models import (
#     EntryCategory,
#     EntryTag,
#     Entry,
#     EntryLink,
#     Post,
#     Project,
#     Tutorial,
# )


# @admin.register(EntryCategory)
# class EntryCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "order", "slug")
#     prepopulated_fields = {"slug": ("name",)}
#     ordering = ("order",)


# @admin.register(EntryTag)
# class EntryTagAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug")
#     prepopulated_fields = {"slug": ("name",)}


# class EntryLinkInline(admin.TabularInline):
#     model = EntryLink
#     extra = 1


# # -------------------
# # Base admin for proxies
# # -------------------
# class BaseEntryAdmin(admin.ModelAdmin):
#     list_display = ("title", "status", "author", "is_featured", "created_at", "updated_at")
#     list_filter = ("status", "categories", "tags", "is_featured", "difficulty", "created_at")
#     search_fields = ("title", "excerpt", "body")
#     prepopulated_fields = {"slug": ("title",)}
#     inlines = [EntryLinkInline]
#     filter_horizontal = ("categories", "tags")
#     readonly_fields = ("reading_time", "likes_count", "created_at", "updated_at")
#     date_hierarchy = "created_at"
#     exclude = ("type",)  # don’t show type in admin form

#     # Filter queryset to only include this proxy's type
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.filter(type=self.entry_type)

#     # Auto-assign type when saving
#     def save_model(self, request, obj, form, change):
#         obj.type = self.entry_type
#         super().save_model(request, obj, form, change)


# # -------------------
# # Proxy model admins
# # -------------------
# @admin.register(Post)
# class PostAdmin(BaseEntryAdmin):
#     entry_type = "post"


# @admin.register(Project)
# class ProjectAdmin(BaseEntryAdmin):
#     entry_type = "project"


# @admin.register(Tutorial)
# class TutorialAdmin(BaseEntryAdmin):
#     entry_type = "tutorial"


# # -------------------
# # EntryLink admin
# # -------------------
# @admin.register(EntryLink)
# class EntryLinkAdmin(admin.ModelAdmin):
#     list_display = ("title", "entry", "link_type", "url")
#     list_filter = ("link_type", "entry")
#     search_fields = ("title", "url")
from django.utils.html import format_html
from django.contrib import admin
from .models import (
    EntryTag,
    Entry,
    EntryLink,
    Post,
    Project,
    Material,
    EntryMaterial,
    DesignAsset,
)

# -------------------
# Tag admin
# -------------------
@admin.register(EntryTag)
class EntryTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# -------------------
# Material admin
# -------------------
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_preview", "url")
    search_fields = ("name", "url")

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" style="object-fit:contain;"/>', obj.icon.url)
        return "-"
    icon_preview.short_description = "Icon"


# -------------------
# Inlines
# -------------------
class EntryLinkInline(admin.TabularInline):
    model = EntryLink
    extra = 1


class EntryMaterialInline(admin.TabularInline):
    model = EntryMaterial
    extra = 1
    autocomplete_fields = ("material",)


class DesignAssetInline(admin.TabularInline):
    model = DesignAsset
    extra = 1


# -------------------
# Base admin for Entry proxies
# -------------------
class BaseEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "author", "is_featured", "created_at", "updated_at")
    list_filter = ("status", "tags", "is_featured", "difficulty", "created_at")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EntryLinkInline, EntryMaterialInline, DesignAssetInline]
    filter_horizontal = ("tags",)
    readonly_fields = ("reading_time", "created_at", "updated_at")
    date_hierarchy = "created_at"
    exclude = ("type",)

    # Filter queryset to only include this proxy's type
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type=self.entry_type)

    # Auto-assign type when saving
    def save_model(self, request, obj, form, change):
        obj.type = self.entry_type
        super().save_model(request, obj, form, change)


# -------------------
# Proxy model admins
# -------------------
@admin.register(Post)
class PostAdmin(BaseEntryAdmin):
    entry_type = "post"


@admin.register(Project)
class ProjectAdmin(BaseEntryAdmin):
    entry_type = "project"


# -------------------
# EntryLink admin
# -------------------
@admin.register(EntryLink)
class EntryLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "entry", "link_type", "url")
    list_filter = ("link_type", "entry")
    search_fields = ("title", "url")


# -------------------
# DesignAsset admin
# -------------------
@admin.register(DesignAsset)
class DesignAssetAdmin(admin.ModelAdmin):
    list_display = ("title", "asset_type", "entry")
    list_filter = ("asset_type",)
    search_fields = ("title", "description")
