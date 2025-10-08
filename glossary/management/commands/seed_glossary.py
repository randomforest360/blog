from django.core.management.base import BaseCommand
from glossary.models import Term
from faker import Faker
import random
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Seed the glossary with fake terms."

    def add_arguments(self, parser):
        parser.add_argument('--terms', type=int, default=50, help='Number of fake terms to create')

    def handle(self, *args, **options):
        fake = Faker()
        count = options['terms']

        self.stdout.write(f"🌱 Seeding {count} glossary terms...")

        for _ in range(count):
            term_name = fake.unique.word().capitalize()
            definition = fake.paragraph(nb_sentences=3)
            
            # Optional URL (50% chance)
            url = fake.url() if random.random() < 0.5 else None
            
            # Optional image placeholder (50% chance)
            image = f"glossary_images/{term_name.lower()}.png" if random.random() < 0.5 else None

            term = Term.objects.create(
                term=term_name,
                definition=definition,
                slug=slugify(term_name),
                url=url,
                image=image
            )
            self.stdout.write(f"✅ Created: {term.term} (Letter: {term.alphabet})")

        self.stdout.write(self.style.SUCCESS(f"🎉 Successfully seeded {count} terms!"))

