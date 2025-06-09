from django.core.management.base import BaseCommand
from store.models import ProductImage
import os
import shutil

class Command(BaseCommand):
    help = 'Clean up media directory and database by removing duplicate images'

    def handle(self, *args, **options):
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        media_dir = os.path.join(project_root, 'media', 'products')
        
        if os.path.exists(media_dir):
            # Delete all files in the media directory
            for filename in os.listdir(media_dir):
                file_path = os.path.join(media_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        self.stdout.write(self.style.SUCCESS(f"Deleted file: {filename}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error deleting {filename}: {str(e)}"))
        
        # Delete all ProductImage entries from the database
        ProductImage.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Cleared all product images from database"))
        
        self.stdout.write(self.style.SUCCESS("Cleanup completed successfully")) 