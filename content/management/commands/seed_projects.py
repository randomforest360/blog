from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from content.models import Entry, EntryCategory, EntryTag
from django.utils.text import slugify
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Populate demo projects with Faker and randomized tag-category linking"

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No user found. Create a user first."))
            return

        # Create categories if none exist
        category_names = ["Frontend", "Backend", "Data Science", "DevOps", "Mobile"]
        category_objs = {}
        for name in category_names:
            category, _ = EntryCategory.objects.get_or_create(name=name, slug=slugify(name))
            category_objs[name] = category

        self.stdout.write(self.style.SUCCESS("✅ Categories ensured."))

        # Create tags and link random subsets to categories
        tag_map = {
            "Frontend": ["JavaScript", "React", "CSS", "HTML", "Vue"],
            "Backend": ["Python", "Django", "Node.js"],
            "Data Science": ["Pandas", "NumPy", "Scikit-learn"],
            "DevOps": ["Docker", "Kubernetes", "CI/CD"],
            "Mobile": ["Flutter", "Swift", "Kotlin"],
        }

        created_tags = {}

        for category_name, tag_list in tag_map.items():
            category = category_objs[category_name]
            selected_tag_names = random.sample(tag_list, random.randint(2, len(tag_list)))  # pick 2 to all tags
            for tag_name in selected_tag_names:
                tag_slug = slugify(tag_name)
                tag, _ = EntryTag.objects.get_or_create(name=tag_name, slug=tag_slug)
                tag.categories.add(category)
                created_tags.setdefault(category_name, []).append(tag)

        self.stdout.write(self.style.SUCCESS("🏷 Tags created and randomly linked to categories."))

        # Create demo entries
        for i in range(10):
            title = fake.sentence(nb_words=6)
            entry = Entry.objects.create(
                title=title,
                slug=slugify(f"{title}-{random.randint(1000,9999)}"),
                body=fake.paragraph(nb_sentences=10),
                type="project",
                status="published",
                author=user,
                excerpt=fake.text(max_nb_chars=150),
                difficulty=random.choice(["beginner", "intermediate", "advanced"]),
                is_featured=random.choice([True, False]),
                progress_percent=random.randint(0, 100),
                cover_alt=fake.sentence(nb_words=5),
                likes_count=random.randint(0, 500),
            )

            # Assign one category
            category_name = random.choice(category_names)
            category = category_objs[category_name]
            entry.categories.add(category)

            # Assign tags linked to that category
            category_tags = created_tags.get(category_name, [])
            if category_tags:
                entry.tags.add(*random.sample(category_tags, min(len(category_tags), 3)))

            self.stdout.write(self.style.SUCCESS(f"📦 Created project: {entry.title}"))
