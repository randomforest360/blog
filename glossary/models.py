from django.db import models
from django.urls import reverse

class Term(models.Model):
    """Glossary term with optional link, image, and alphabet category"""
    term = models.CharField(max_length=200, unique=True)
    definition = models.TextField()
    slug = models.SlugField(unique=True)
    url = models.URLField(blank=True, null=True, help_text="Optional external link")
    image = models.ImageField(upload_to="glossary_images/", blank=True, null=True, help_text="Optional image")
    alphabet = models.CharField(max_length=1, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['term']

    def __str__(self):
        return self.term

    def get_absolute_url(self):
        return reverse("glossary:term_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if self.term:
            self.alphabet = self.term[0].upper()
        super().save(*args, **kwargs)


# python manage.py dumpdata glossary --indent 4 > backup/glossary_backup.json
# python manage.py loaddata backup/glossary_backup.json
