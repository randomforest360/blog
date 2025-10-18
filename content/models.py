from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.contrib.auth.models import User
from core.models import RelatedItem
from django.contrib.contenttypes.fields import GenericRelation
import math
from django.urls import reverse

# -------------------
# Materials
# -------------------
class Material(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    icon = models.ImageField(upload_to="material_icons/", blank=True, null=True)

    def __str__(self):
        return self.name


class EntryMaterial(models.Model):
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ("entry", "material")

    def __str__(self):
        return f"{self.quantity or ''} {self.material.name}".strip()


# -------------------
# Tags
# -------------------
class EntryTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Entry Tags"

    def __str__(self):
        return self.name


# -------------------
# Entry (Core Model)
# -------------------
class Entry(models.Model):
    CONTENT_TYPES = [
        ('project', 'Project'),
        ('post', 'Post'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    materials = models.ManyToManyField(Material, through=EntryMaterial, related_name="entries")
    tags = models.ManyToManyField(EntryTag, blank=True, related_name="entry_tags")
    related_items = GenericRelation(RelatedItem)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='post')
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    body = RichTextUploadingField()
    excerpt = models.CharField(max_length=160, blank=True, help_text="Short summary or description for previews and SEO")
    cover = models.ImageField(upload_to="entry_images/", blank=True, null=True)
    cover_alt = models.CharField(max_length=150, blank=True, help_text="Accessible alt text for cover image")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, blank=True, null=True)
    reading_time = models.PositiveIntegerField(default=0, editable=False, help_text="Estimated reading time in minutes")


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Entry.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        if self.type == 'project':
            return reverse('project_detail', kwargs={'slug': self.slug})
        elif self.type == 'post':
            return reverse('post_detail', kwargs={'slug': self.slug})
        else:
            raise ValueError(f"Unknown entry type: {self.type}")

    @property
    def is_visible(self):
        return self.status == 'published'

    @property
    def show_as_featured(self):
        return self.status == 'published' and self.is_featured


# -------------------
# Related Links
# -------------------
class EntryLink(models.Model):
    LINK_TYPES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('demo', 'Demo'),
        ('reference', 'Reference'),
    ]
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="links")
    title = models.CharField(max_length=100)
    url = models.URLField()
    link_type = models.CharField(max_length=20, choices=LINK_TYPES, default='reference')
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class (e.g. 'bi bi-rocket')")


    def __str__(self):
        return f"{self.title} ({self.entry.title})"

# -------------------
# Design Assets
# -------------------
class DesignAsset(models.Model):
    ASSET_TYPES = [
        ("diagram", "Diagram"),
        ("3d_model", "3D Model"),
        ("circuit", "Circuit"),
        ("architecture", "Architecture"),
        ("other", "Other"),
    ]

    entry = models.ForeignKey("Entry", on_delete=models.CASCADE, related_name="assets")
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to="design_assets/")
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, default="other")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.asset_type})"


# -------------------
# Proxy Models (admin separation)
# -------------------
class Post(Entry):
    class Meta:
        proxy = True
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Project(Entry):
    class Meta:
        proxy = True
        verbose_name = "Project"
        verbose_name_plural = "Projects"