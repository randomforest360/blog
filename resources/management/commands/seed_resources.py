from django.core.management.base import BaseCommand
from faker import Faker
import random

from resources.models import Resource, ResourceCategory

class Command(BaseCommand):
    help = "Seed the database with dummy resources and categories."

    def add_arguments(self, parser):
        parser.add_argument('--categories', type=int, default=5, help='Number of categories to create')
        parser.add_argument('--resources', type=int, default=20, help='Number of resources to create')

    def handle(self, *args, **options):
        fake = Faker()
        num_categories = options['categories']
        num_resources = options['resources']

        # Delete existing data
        Resource.objects.all().delete()
        ResourceCategory.objects.all().delete()
        self.stdout.write(self.style.WARNING("⚠️ Deleted all existing resources and categories."))

        # Create categories
        categories = []
        for _ in range(num_categories):
            cat_name = fake.word().capitalize() + " Tools"
            cat_slug = fake.unique.slug()
            category = ResourceCategory.objects.create(name=cat_name, slug=cat_slug)
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))

        # Create resources
        for _ in range(num_resources):
            title = fake.sentence(nb_words=4)
            url = fake.url()
            description = fake.paragraph(nb_sentences=3)
            category = random.choice(categories) if categories else None
            tags = ", ".join([fake.word() for _ in range(random.randint(1,4))])
            is_featured = random.choice([True, False])

            resource = Resource.objects.create(
                title=title,
                url=url,
                description=description,
                category=category,
                tags=tags,
                is_featured=is_featured
            )
            self.stdout.write(self.style.SUCCESS(f"Created resource: {resource.title}"))
        
        self.stdout.write(self.style.SUCCESS("✅ Done seeding resources!"))
