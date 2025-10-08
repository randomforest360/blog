# core/models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class RelatedItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Related Item"
        verbose_name_plural = "Related Items"

    def __str__(self):
        return f"RelatedItem: {self.content_object}"


from django.db import models

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("twitter", "Twitter"),
        ("mastodon", "Mastodon"),
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()
    is_visible = models.BooleanField(default=True, help_text="Check to display this link on the site")

    ICON_MAP = {
        "github": "bi-github",
        "linkedin": "bi-linkedin",
        "twitter": "bi-twitter-x",
        "mastodon": "bi-mastodon",
    }

    @property
    def icon_class(self):
        return self.ICON_MAP.get(self.platform, "bi-link-45deg")

    def __str__(self):
        return f"{self.get_platform_display()}"



class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  # becomes True after verification
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email