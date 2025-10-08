import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from glossary.models import Term  # adjust import if your app is named differently

class Command(BaseCommand):
    help = 'Import glossary terms from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file to import',
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        count = 0
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                term_text = row['Term'].strip()
                definition = row['Definition'].strip()
                url = row.get('URL', '').strip() or None
                image = row.get('Image', '').strip() or None
                slug = row.get('Slug', '').strip() or slugify(term_text)

                Term.objects.update_or_create(
                    term=term_text,
                    defaults={
                        'definition': definition,
                        'slug': slug,
                        'url': url,
                        'image': image,
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} terms!'))
