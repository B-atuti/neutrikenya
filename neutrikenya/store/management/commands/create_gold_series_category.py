from django.core.management.base import BaseCommand
from store.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create Gold Series category'

    def handle(self, *args, **options):
        category_name = 'Gold Series'
        category_slug = slugify(category_name)
        
        # Ensure unique slug
        counter = 1
        while Category.objects.filter(slug=category_slug).exists():
            category_slug = f"{slugify(category_name)}-{counter}"
            counter += 1
        
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={
                'slug': category_slug,
                'description': 'Premium skincare products infused with gold particles and luxurious ingredients to provide anti-aging benefits, enhance skin radiance, and deliver exceptional results for a more youthful, glowing complexion.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created category: {category.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Category already exists: {category.name}")) 