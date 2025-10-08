from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.contrib.auth.models import User
from core.models import RelatedItem
from django.contrib.contenttypes.fields import GenericRelation
import math
from django.urls import reverse

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



class EntryCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Entry Categories"

    def __str__(self):
        return self.name

# class EntryTag(models.Model):
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(unique=True)

#     def __str__(self):
#         return self.name

class EntryTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(EntryCategory, related_name="tags", blank=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    CONTENT_TYPES = [
        ('project', 'Project'),
        ('tutorial', 'Tutorial'),
        ('post', 'Post'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'), # idea stage
        ('in_progress', 'In Progress'), # actively being written
        ('published', 'Published'), # public and polished
        ('archived', 'Archived'), # hidden from users, but kept in the system
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    materials = models.ManyToManyField(Material, through=EntryMaterial, related_name="entries")
    type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='post')
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    body = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    excerpt = models.CharField(max_length=160, blank=True, help_text="Short summary or description for previews and SEO")
    categories = models.ManyToManyField(EntryCategory, related_name="entry_categories")
    tags = models.ManyToManyField(EntryTag, blank=True, related_name="entry_tags")
    cover = models.ImageField(upload_to="entry_images/", blank=True, null=True)
    cover_alt = models.CharField(max_length=150, blank=True, help_text="Accessible alt text for cover image")  
    related_items = GenericRelation(RelatedItem)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    progress_percent = models.PositiveSmallIntegerField(default=0, help_text="0–100% progress (only shown if status is 'in progress')")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, blank=True, null=True)
    reading_time = models.PositiveIntegerField(default=0, editable=False, help_text="Estimated reading time in minutes")
    likes_count = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        word_count = len(self.body.split())
        self.reading_time = max(1, math.ceil(word_count / 200))
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     # You can make this dynamic based on type if needed
    #     return reverse('project_detail', kwargs={'slug': self.slug})
    
    def get_absolute_url(self):
        if self.type == 'project':
            return reverse('project_detail', kwargs={'slug': self.slug})
        elif self.type == 'tutorial':
            return reverse('tutorial_detail', kwargs={'slug': self.slug})
        elif self.type == 'post':
            return reverse('post_detail', kwargs={'slug': self.slug})
        # fallback if type is somehow invalid
        return reverse('project_detail', kwargs={'slug': self.slug})

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


class EntryLike(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="likes")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['entry', 'ip_address', 'session_key'],
                name='unique_anon_like'
            ),
        ]

    def __str__(self):
        return f"Anonymous like on {self.entry.title}"
# MAX_LIKES_PER_ENTRY = 1_000
# You could even use the like count to:

# Auto-feature entries that hit 500+ likes

# Send yourself a notification when something hits a threshold

# Display a “🔥 Popular” badge once it crosses a certain number
# -------------------
# Likes
# -------------------
# class EntryLike(models.Model):
#     entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="likes")
#     ip_address = models.GenericIPAddressField(blank=True, null=True)
#     session_key = models.CharField(max_length=40, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['entry', 'ip_address', 'session_key'],
#                 name='unique_anon_like'
#             ),
#         ]

#     def __str__(self):
#         return f"Anonymous like on {self.entry.title}"

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


class Tutorial(Entry):
    class Meta:
        proxy = True
        verbose_name = "Tutorial"
        verbose_name_plural = "Tutorials"



# If you want to allow tags to belong to multiple categories, you’d use a ManyToManyField instead of ForeignKey. But for most cases, one-to-one linking is simpler and cleaner.