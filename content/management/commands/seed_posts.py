from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from content.models import Entry, EntryCategory, EntryTag
from django.utils.text import slugify
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Populate demo blog posts with Faker"

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        categories = list(EntryCategory.objects.all())
        tags = list(EntryTag.objects.all())

        for i in range(15):
            title = fake.sentence(nb_words=8)
            entry = Entry.objects.create(
                title=title,
                slug=slugify(f"{title}-{random.randint(1000,9999)}"),
                body=fake.paragraph(nb_sentences=15),
                type="post",
                status="published",
                author=user,
                excerpt=fake.text(max_nb_chars=160),
                is_featured=random.choice([True, False]),
                cover_alt=fake.sentence(nb_words=6),
                likes_count=random.randint(0, 1000),
            )
            if categories:
                entry.categories.add(random.choice(categories))
            if tags:
                entry.tags.add(*random.sample(tags, min(len(tags), 5)))

            self.stdout.write(self.style.SUCCESS(f"Created post: {entry.title}"))
