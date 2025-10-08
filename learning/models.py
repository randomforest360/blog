# learning/models.py
from django.db import models
from django.urls import reverse
from lab.models import LabItem
# from projects.models import Project
# from tutorials.models import Tutorial

class LearningPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=100)  # e.g., HTML, React, Python
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("learning:path_detail", args=[self.slug])


class Lesson(models.Model):
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()  # step number
    content = models.TextField(blank=True)  # tutorial content or instructions

    # Optional links to other apps
    # tutorial = models.ForeignKey(Tutorial, blank=True, null=True, on_delete=models.SET_NULL)
    lab_item = models.ForeignKey(LabItem, blank=True, null=True, on_delete=models.SET_NULL)
    # project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.path.title} - Step {self.order}: {self.title}"


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="quiz")
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.lesson.title} - Quiz"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=300)
    options = models.JSONField()  # multiple-choice options
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.quiz.title} - Question: {self.question_text[:50]}"
