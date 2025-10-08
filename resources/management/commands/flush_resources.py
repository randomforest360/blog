from django.core.management.base import BaseCommand
from resources.models import Resource, ResourceCategory

class Command(BaseCommand):
    help = "Delete all resources and categories."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("⚠️  Deleting all resources and categories..."))

        Resource.objects.all().delete()
        ResourceCategory.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ All resources and categories have been deleted."))
