from django.db import models
from django.urls import reverse

class ResourceCategory(models.Model):
    """Optional category for grouping resources, e.g., 'Color', 'Images', 'CSS Tools'."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Resource Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("resources:category_detail", args=[self.slug])


class Resource(models.Model):
    """Represents a single useful website/tool/resource."""
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="resources")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags, e.g., 'palette,color,css'")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: show in homepage or featured
    # is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("resources:detail", args=[self.id])
