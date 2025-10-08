from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from content.models import Entry, EntryCategory, EntryTag, EntryLink
from faker import Faker
import random


class Command(BaseCommand):
    help = "Populate Entries, Categories, Tags, and Links with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create some users if none exist
        if User.objects.count() == 0:
            for _ in range(3):
                User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password="password123"
                )

        users = list(User.objects.all())

        # Create categories
        categories = []
        for name in ["Hardware", "Software", "Raspberry Pi", "Retro Tech", "DIY"]:
            cat, _ = EntryCategory.objects.get_or_create(
                name=name,
                slug=name.lower().replace(" ", "-")
            )
            categories.append(cat)

        # Create tags
        tags = []
        for name in ["Python", "Arduino", "Electronics", "Guide", "Tutorial"]:
            tag, _ = EntryTag.objects.get_or_create(
                name=name,
                slug=name.lower()
            )
            tags.append(tag)

        # Create entries
        for _ in range(15):
            title = fake.sentence(nb_words=5).rstrip(".")

            # Generate structured HTML with headings and paragraphs
            body_parts = []
            for i in range(random.randint(2, 3)):  # 2–3 H2 sections
                body_parts.append(f"<h2>{fake.sentence(nb_words=4)}</h2>")
                body_parts.extend([f"<p>{para}</p>" for para in fake.paragraphs(nb=random.randint(2, 4))])

                # Insert one H3 under the first H2
                if i == 0:
                    body_parts.append(f"<h3>{fake.sentence(nb_words=5)}</h3>")
                    body_parts.extend([f"<p>{para}</p>" for para in fake.paragraphs(nb=2)])

            body_html = "\n".join(body_parts)

            entry = Entry.objects.create(
                title=title,
                slug=title.lower().replace(" ", "-"),
                body=body_html,
                author=random.choice(users),
                excerpt=fake.text(max_nb_chars=100),
                type=random.choice(['post', 'project', 'tutorial']),
                status=random.choice(["draft", "in_progress", "published", "archived"]),
                progress_percent=random.randint(0, 100),
                difficulty=random.choice(["beginner", "intermediate", "advanced"]),
                is_featured=random.choice([True, False]),
                cover_alt=fake.sentence(nb_words=5)
            )

            # Assign random categories and tags
            entry.categories.set(random.sample(categories, random.randint(1, 2)))
            entry.tags.set(random.sample(tags, random.randint(1, 3)))

            # Add some links
            for link_type in ["frontend", "backend", "demo"]:
                if random.choice([True, False]):
                    EntryLink.objects.create(
                        entry=entry,
                        title=fake.word().capitalize(),
                        url=fake.url(),
                        link_type=link_type
                    )

        self.stdout.write(self.style.SUCCESS("✅ Successfully populated Entries with headings, Categories, Tags, and Links!"))
