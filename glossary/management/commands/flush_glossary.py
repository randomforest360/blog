from django.core.management.base import BaseCommand
from glossary.models import Term

class Command(BaseCommand):
    help = "Delete all glossary terms."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("⚠️  Deleting all glossary terms..."))

        Term.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ All glossary terms have been deleted."))
