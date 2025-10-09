# lab/models.py
from django.db import models
from django.urls import reverse

class LabItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    html_code = models.TextField(blank=True)
    css_code = models.TextField(blank=True)
    js_code = models.TextField(blank=True)
    
    # author = models.CharField(max_length=100, blank=True)
    # reference_link = models.URLField(blank=True, null=True)
    
    # related_blog = models.ForeignKey('blog.BlogPost', blank=True, null=True, on_delete=models.SET_NULL)
    # related_project = models.ForeignKey('projects.Project', blank=True, null=True, on_delete=models.SET_NULL)
    
    # tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return self.title
    
    # def get_absolute_url(self):
    #     return reverse("lab:lab_detail", args=[str(self.id)])
