# learning/management/commands/flush_learning.py
from django.core.management.base import BaseCommand
from learning.models import LearningPath, Lesson, Quiz, Question


class Command(BaseCommand):
    help = "Delete all LearningPath, Lesson, Quiz, and Question data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("⚠️  Deleting all learning-related data..."))

        Question.objects.all().delete()
        Quiz.objects.all().delete()
        Lesson.objects.all().delete()
        LearningPath.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ All learning-related data has been deleted."))
