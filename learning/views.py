# learning/views.py
from django.shortcuts import render, get_object_or_404
from .models import LearningPath, Lesson

def path_list(request):
    paths = LearningPath.objects.all()
    return render(request, "learning/path_list.html", {"paths": paths})

def path_detail(request, slug):
    path = get_object_or_404(LearningPath, slug=slug)
    return render(request, "learning/path_detail.html", {"path": path})

def lesson_detail(request, path_slug, order):
    lesson = get_object_or_404(Lesson, path__slug=path_slug, order=order)
    return render(request, "learning/lesson_detail.html", {"lesson": lesson})
# 6️⃣ Optional Features / Enhancements

# Progress tracking → save completed lessons/quizzes per user.

# Integrate Lab live editors directly in lesson pages.

# Tags or filtering → filter paths by topic or difficulty.

# Nested quizzes → allow interactive testing at each step.

# Certificates / achievements → optional gamification.

# ✅ Summary

# Your learning app:

# Central hub for curated step-by-step learning paths.

# Lessons can reference tutorials, lab items, or projects.

# Quizzes are associated with lessons.

# Flexible and expandable, ready for integration with Blog, Lab, Projects, Tutorials.