# learning/management/commands/seed_learning.py
from django.core.management.base import BaseCommand
from faker import Faker
import random

from learning.models import LearningPath, Lesson, Quiz, Question
from lab.models import LabItem
# from tutorials.models import Tutorial
# from projects.models import Project


class Command(BaseCommand):
    help = "Seed the database with dummy learning paths, lessons, quizzes, and questions."

    def add_arguments(self, parser):
        parser.add_argument('--paths', type=int, default=3, help='Number of learning paths to create')
        parser.add_argument('--lessons', type=int, default=5, help='Lessons per learning path')
        parser.add_argument('--questions', type=int, default=3, help='Questions per lesson quiz')

    def handle(self, *args, **options):
        fake = Faker()

        num_paths = options['paths']
        lessons_per_path = options['lessons']
        questions_per_quiz = options['questions']

        self.stdout.write(self.style.SUCCESS("Seeding database..."))

        for _ in range(num_paths):
            path = LearningPath.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                topic=random.choice(["HTML", "CSS", "JavaScript", "Python", "Django", "React"]),
                slug=fake.unique.slug(),
            )
            self.stdout.write(self.style.SUCCESS(f"Created LearningPath: {path.title}"))

            for lesson_order in range(1, lessons_per_path + 1):
                lesson = Lesson.objects.create(
                    path=path,
                    title=fake.sentence(nb_words=6),
                    order=lesson_order,
                    content=fake.text(max_nb_chars=500),
                    lab_item=LabItem.objects.order_by("?").first() if LabItem.objects.exists() else None,
                )

                # Create ONE quiz per lesson
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=f"Quiz for {lesson.title}"
                )

                # Add multiple questions to that quiz
                for _ in range(questions_per_quiz):
                    options = [fake.word() for _ in range(4)]
                    correct = random.choice(options)
                    Question.objects.create(
                        quiz=quiz,
                        question_text=fake.sentence(nb_words=10),
                        options=options,
                        correct_answer=correct
                    )

        self.stdout.write(self.style.SUCCESS("✅ Done seeding learning data!"))
