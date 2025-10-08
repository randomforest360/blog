# learning/admin.py
from django.contrib import admin
from .models import LearningPath, Lesson, Quiz, Question
from lab.models import LabItem

# -----------------------------
# Question Inline for Quiz
# -----------------------------
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3  # show 3 empty question forms by default
    fields = ('question_text', 'options', 'correct_answer')
    readonly_fields = ()
    show_change_link = True

# -----------------------------
# Quiz Inline for Lesson
# -----------------------------
class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 1  # only one quiz allowed per lesson
    max_num = 1
    inlines = [QuestionInline]  # optional: you can't nest inlines directly
    fields = ('title',)
    show_change_link = True

# -----------------------------
# Lesson Admin
# -----------------------------
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'order')
    list_filter = ('path',)
    search_fields = ('title', 'content')
    ordering = ('path', 'order')
    inlines = [QuizInline]

# -----------------------------
# LearningPath Admin
# -----------------------------
@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at')
    search_fields = ('title', 'description', 'topic')
    prepopulated_fields = {'slug': ('title',)}

# -----------------------------
# Quiz Admin (Optional)
# -----------------------------
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson')
    search_fields = ('title',)
    inlines = [QuestionInline]

# -----------------------------
# Question Admin
# -----------------------------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('question_text',)
