from django.core.management.base import BaseCommand
from content.models import (
    Entry,
    EntryCategory,
    EntryTag,
    EntryLink,
    Material,
    EntryMaterial,
    # EntryLike,  # Uncomment if using this model
)

class Command(BaseCommand):
    help = "Delete all content-related models: Entries, Categories, Tags, Materials, Links, and more"

    def handle(self, *args, **kwargs):
        # Delete in safe order to avoid foreign key issues
        EntryLink.objects.all().delete()
        EntryMaterial.objects.all().delete()
        Entry.objects.all().delete()
        EntryCategory.objects.all().delete()
        EntryTag.objects.all().delete()
        Material.objects.all().delete()
        # EntryLike.objects.all().delete()  # Uncomment if using

        self.stdout.write(self.style.WARNING("🧹 All content-related data has been deleted:"))
        self.stdout.write("• Entries")
        self.stdout.write("• EntryLinks")
        self.stdout.write("• EntryMaterials")
        self.stdout.write("• EntryCategories")
        self.stdout.write("• EntryTags")
        self.stdout.write("• Materials")
        # self.stdout.write("• EntryLikes")  # Uncomment if using
